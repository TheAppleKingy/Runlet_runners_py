import yaml

from gateway.infra.services.docker import DockerService
from gateway.infra.configs import RunnersConfig


with open("runners_conf.yaml", "r") as f:
    data = yaml.safe_load(f)

c = RunnersConfig.model_validate(data)
service = DockerService(c)
service._ensure_runner("py")
