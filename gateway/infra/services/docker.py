from typing import TypedDict, Literal, Optional

from docker import from_env
from docker.errors import ImageNotFound

from gateway.application.interfaces.services import (
    DockerServiceInterface,
    CodeRunServiceInterface
)
from gateway.infra.configs import RunnersConfig


class DockerService(DockerServiceInterface):
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
            buildargs=build_args
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

    def run_runner(
        self,
        for_lang: str,
        cmd: list[str],
    ):
        if not self._ensure_image(for_lang):
            self.build(for_lang)
