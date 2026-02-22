import os
import tempfile
import json

from dishka.integrations.celery import FromDishka, inject

from gateway.application.interfaces import CodeRunnerInterface
from gateway.application.interfaces import MessagePublisherInterface
from gateway.application.dtos import (
    ResultDTO,
    DictTestSolutionDTO,
    TestCaseDTO
)
from gateway.celery_app import celery_app
from gateway.logger import logger


@celery_app.task
def test_solution(
    dto: DictTestSolutionDTO,
    runner: FromDishka[CodeRunnerInterface],
    publisher: FromDishka[MessagePublisherInterface]
):
    file_name = f"run-s-{dto['student_id']}-p-{dto['problem_id']}.json"
    path = os.path.join(tempfile.gettempdir(), file_name)
    with open(path, "w") as f:
        json.dump({"code": dto["code"], "run_data": dto["run_data"]}, f)
    try:
        result = runner.run_code(dto["lang"], path, len(dto["run_data"]))
        result_model = ResultDTO.model_validate_json(result)
        if not result_model.test_cases:
            err_msg = result_model.err_msg or "internal error: tests didn't run and error message not given"
            head_err = err_msg.split(": ")[0]
            result_model.test_cases = [TestCaseDTO(**{**dto["run_data"][0], "output": head_err})]
            logger.error(
                f"Unable to run tests of problem {dto["problem_id"]} by student {dto["student_id"]}. Runner response - '{result_model.err_msg}'")
        publisher.publish(result_model.model_dump_json())
    except Exception as e:
        publisher.publish(
            ResultDTO(test_cases=[
                TestCaseDTO(**{**dto["run_data"][0], "output": "internal error"})
            ]).model_dump_json()
        )
        logger.exception(
            f"Error occured when try to run tests of problem {dto['problem_id']} by student {dto['student_id']} occured: {e}")
    finally:
        os.remove(path)
