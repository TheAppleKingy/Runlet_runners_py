import yaml
import asyncio

from gateway.infra.services.code_runner import DockerCodeRunService
from gateway.infra.configs import RunnersConfig
from gateway.application.use_case import TestSolutionUseCase, TestSolutionDTO
from gateway.application.dtos import RunDataDTO


with open("config.yaml", "r") as f:
    data = yaml.safe_load(f)

m = RunnersConfig.model_validate(data)
s = DockerCodeRunService(m)
uc = TestSolutionUseCase(s)
run_data = [RunDataDTO(test_num=1, input="1 2"), RunDataDTO(test_num=2, input="3 4")]
code = """
import time


time.sleep(5)


print("CPU test completed")
"""
dto = TestSolutionDTO(
    student_id=1,
    problem_id=2,
    lang="py",
    code=code,
    run_data=run_data
)

if __name__ == "__main__":
    res = asyncio.run(uc.execute(dto))
    print(res)
