import os
import tempfile
import json
import aiofiles

from gateway.application.interfaces.services import CodeRunnerInterface
from .dtos import (
    TestSolutionDTO,
    ResultDTO,
    InputDTO
)
from .errors import TestSolutionError


class TestSolutionUseCase:
    def __init__(self, run_service: CodeRunnerInterface):
        self._run_service = run_service

    async def execute(self, dto: TestSolutionDTO):
        file_name = f"run-s-{dto.student_id}-p-{dto.problem_id}.json"
        path = os.path.join(tempfile.gettempdir(), file_name)
        async with aiofiles.open(path, "w") as f:
            await f.write(InputDTO(code=dto.code, run_data=dto.run_data).model_dump_json())
        try:
            result = self._run_service.run_code(dto.lang, path, len(dto.run_data))
            model = ResultDTO.model_validate_json(result)
            return model
        except Exception as e:
            raise TestSolutionError(
                f"Error occured when solution of problem {dto.problem_id} by student {dto.student_id} occured: {e}")
        finally:
            os.remove(path)
