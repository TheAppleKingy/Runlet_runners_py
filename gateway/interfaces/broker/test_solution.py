from ploomby.registry import HandlersRegistry

from gateway.application.dtos import TestSolutionDTO

gateway_registry = HandlersRegistry()


@gateway_registry.register()
async def test_solution(dto: TestSolutionDTO):
    pass
