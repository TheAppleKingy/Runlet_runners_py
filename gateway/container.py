from dishka import (
    make_container,
    provide,
    Provider,
    Scope
)
from gateway.infra.configs import RabbitConfig


class RunnerGatewayProvider(Provider):
    scope = Scope.APP

    @provide
    def rabbit_conf(self) -> RabbitConfig:
        return RabbitConfig()  # type: ignore[call-arg]


container = make_container(RunnerGatewayProvider())
