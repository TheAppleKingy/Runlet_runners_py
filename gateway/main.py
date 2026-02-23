import asyncio
import signal

from dishka.integrations.celery import setup_dishka
from ploomby.registry import MessageConsumerRegistry
from ploomby.rabbit import RabbitConsumerFactory

from gateway.interfaces.broker.test_solution import gateway_registry
from gateway.logger import logger
from gateway.container import container
from gateway.infra.configs import RabbitConfig
from gateway.celery_app import celery_app

running = True


def stop_run(signum=None, frame=None):
    global running
    running = False


signal.signal(signal.SIGINT, stop_run)
signal.signal(signal.SIGTERM, stop_run)


async def lock():
    try:
        counter = 0
        logger.info("Runners gateway is running. Ready to test solutions")
        while running:
            await asyncio.sleep(1)
            counter += 1
            if counter == 120:
                logger.info("Runners gateway is running. Ready to test solutions")
                counter = 0
    except asyncio.CancelledError:
        return


async def lifespan():
    logger.info("Starting runners gateway")
    setup_dishka(container, celery_app)
    rabbit_conf = container.get(RabbitConfig)
    factory = RabbitConsumerFactory(rabbit_conf.conn_url, shared_conn=False)
    consumer_registry = MessageConsumerRegistry(gateway_registry, factory)
    await consumer_registry.register(
        rabbit_conf.incoming_data_queue,
        "task_name",
        prefetch_count=10,
        with_dead_letter_policy=True
    )
    await lock()
    logger.info("Runners gateway stopped.")
    container.close()
    await consumer_registry.disconnect_consumers()


if __name__ == "__main__":
    asyncio.run(lifespan())
