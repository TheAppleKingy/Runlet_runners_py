import yaml
import asyncio
import aio_pika
from gateway.infra.code_runner import DockerCodeRunService
from gateway.infra.configs import RunnersConfig
from gateway.application.dtos import RunDataDTO, TestSolutionDTO


with open("config.yaml", "r") as f:
    data = yaml.safe_load(f)

m = RunnersConfig.model_validate(data)
s = DockerCodeRunService(m)
run_data = [RunDataDTO(test_num=1, input="1 2"), RunDataDTO(test_num=2, input="3 4")]


async def test_publish():
    conn = await aio_pika.connect_robust("amqp://admin:admin@localhost:5672")
    chan = await conn.channel()
    code = 'print("Hello world")'
    dto = TestSolutionDTO(
        student_id=1,
        problem_id=2,
        lang="py",
        code=code,
        run_data=run_data
    )

    await chan.default_exchange.publish(
        aio_pika.Message(body=dto.model_dump_json().encode(), headers={"task_name": "test_solution_handler"}),
        routing_key="test_solutions"
    )
if __name__ == "__main__":
    asyncio.run(test_publish())
