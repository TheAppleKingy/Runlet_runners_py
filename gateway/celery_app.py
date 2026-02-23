import yaml
from celery import Celery  # type: ignore
from celery.signals import worker_process_shutdown  # type: ignore
from dishka import make_container, Provider, provide, Scope, Container
from dishka.integrations.celery import DishkaTask, setup_dishka

from gateway.container import container
from gateway.infra.configs import (
    RabbitConfig,
    AppConfig,
    RedisConfig,
    RunnersConfig
)
from gateway.application.interfaces import (
    MessagePublisherInterface,
    CodeRunnerInterface
)
from gateway.infra import (
    RabbitPublisher,
    DockerCodeRunService
)


class WorkerProvider(Provider):
    scope = Scope.APP

    @provide
    def redis_conf(self) -> RedisConfig:
        return RedisConfig()  # type: ignore

    @provide
    def rabbit_conf(self) -> RabbitConfig:
        return RabbitConfig()

    @provide
    def app_conf(self) -> AppConfig:
        return AppConfig()

    @provide
    def runners_conf(self, app_conf: AppConfig) -> RunnersConfig:
        with open(app_conf.config_path, "r") as f:
            data = yaml.safe_load(f)
        return RunnersConfig.model_validate(data)

    @provide(scope=Scope.REQUEST)
    def publisher(self, rabbit_conf: RabbitConfig) -> MessagePublisherInterface:
        return RabbitPublisher(rabbit_conf.conn_url, rabbit_conf.outcoming_data_queue, rabbit_conf.task_name)

    runner = provide(DockerCodeRunService, provides=CodeRunnerInterface, scope=Scope.REQUEST)


container = make_container(WorkerProvider())


def get_celery():
    celery = Celery(__name__, task_cls=DishkaTask)
    conf = container.get(RedisConfig)
    celery.conf.broker_url = conf.conn_url
    celery.conf.result_backend = conf.conn_url
    celery.autodiscover_tasks(['gateway.infra.tasks.test_solution'])
    setup_dishka(container, celery)
    return celery


celery_app = get_celery()


@worker_process_shutdown.connect()
def _shutdown(*args, **kwargs):
    container: Container = celery_app.conf["dishka_container"]
    container.close()
