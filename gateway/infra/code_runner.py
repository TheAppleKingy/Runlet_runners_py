import json
import os
import uuid

from typing import Optional

from docker import from_env
from docker.errors import ImageNotFound

from gateway.application.interfaces import CodeRunnerInterface
from gateway.infra.configs import RunnersConfig
from gateway.logger import logger


class DockerCodeRunService(CodeRunnerInterface):
    def __init__(
        self,
        runners_conf: RunnersConfig
    ):
        self._cli = from_env()
        self._runners_conf = runners_conf

    def _build(self, dockerfile: str, image_name: str, build_args: Optional[dict] = None):
        self._cli.images.build(
            path=self._runners_conf.context_path,
            dockerfile=f"{self._runners_conf.dockerfiles_path}/{dockerfile}",
            tag=image_name,
            rm=True,
            forcerm=True,
            timeout=60,
            buildargs=build_args,
            nocache=True
        )

    def _check_image(self, image_name: str) -> bool:
        try:
            self._cli.images.get(image_name)
            return True
        except ImageNotFound:
            return False

    def _ensure_shared(self):
        if not self._check_image(self._runners_conf.shared_image_name):
            self._build(
                self._runners_conf.shared_dockerfile_name,
                self._runners_conf.shared_image_name
            )

    def _ensure_runner(self, for_lang: str):
        self._ensure_shared()
        runner_image_name = self._runners_conf.runner_image_name_pattern.format(for_lang)
        if not self._check_image(runner_image_name):
            self._build(
                self._runners_conf.runner_dockerfile_name,
                runner_image_name,
                build_args={"IMAGE": self._runners_conf.runners[for_lang].image}
            )

    def run_code(self, for_lang: str, input_path: str, cases_count: int) -> str:
        self._ensure_runner(for_lang)
        lang_conf = self._runners_conf.runners[for_lang]
        target_file = os.path.basename(input_path)
        cmd = [
            "--run_args", json.dumps(lang_conf.run_args),
            "--compile_args", json.dumps(lang_conf.compile_args),
            "--src_placeholder", self._runners_conf.src_placeholder,
            "--bin_placeholder", self._runners_conf.bin_placeholder,
            "--input", os.path.join(self._runners_conf.runner_mountpoint, target_file),
            "--run_timeout", str(lang_conf.run_timeout)
        ]
        container = self._cli.containers.run(
            image=self._runners_conf.runner_image_name_pattern.format(for_lang),
            command=cmd,
            detach=True,
            mem_limit=lang_conf.mem_limit,
            nano_cpus=int(lang_conf.cpu_cores*1e9),
            network_disabled=True,
            user="sandbox",
            read_only=True,
            security_opt=["no-new-privileges:true"],
            cap_drop=["ALL"],
            pids_limit=100,
            volumes={self._runners_conf.volume_name: {"bind": self._runners_conf.runner_mountpoint, "mode": "ro"}},
            environment=[f"LANG={for_lang}"],
            tmpfs={os.path.split(input_path)[0]: 'rw,noexec,nosuid,nodev,size=10m'},
        )
        try:
            container.wait(timeout=lang_conf.run_timeout * cases_count + 5)
            return container.logs().decode()
        finally:
            container.remove(force=True)
