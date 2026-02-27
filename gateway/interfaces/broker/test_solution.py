from ploomby.registry import HandlersRegistry  # type: ignore[import-untyped]

from gateway.application.dtos import TestSolutionDTO
from gateway.infra.tasks.test_solution import test_solution


gateway_registry = HandlersRegistry()


@gateway_registry.register(key="test_solution")
async def test_solution_handler(dto: TestSolutionDTO):
    test_solution.apply_async(args=[dto.model_dump()], task_id=f"run-s-{dto.student_id}-p-{dto.problem_id}")
