from celery import Celery  # type: ignore
from celery.signals import worker_process_shutdown  # type: ignore
from dishka import make_container, Provider, provide, Scope, Container
from dishka.integrations.celery import DishkaTask, setup_dishka

from gateway.infra.configs import RedisConfig


class WorkerProvider(Provider):
    scope = Scope.APP

    @provide
    def redis_conf(self) -> RedisConfig:
        return RedisConfig()  # type: ignore


container = make_container(WorkerProvider())


def get_celery():
    celery = Celery(__name__, task_cls=DishkaTask)
    conf = container.get(RedisConfig)
    celery.conf.broker_url = conf.conn_url
    celery.conf.result_backend = conf.conn_url
    celery.autodiscover_tasks(['src.infra.tasks.test_solution'])
    setup_dishka(container, celery)
    return celery


celery_app = get_celery()


@worker_process_shutdown.connect()
def _close_container(*args, **kwargs):
    container: Container = celery_app.conf["dishka_container"]
    container.close()
