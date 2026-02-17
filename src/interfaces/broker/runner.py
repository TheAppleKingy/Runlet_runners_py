from ploomby.registry import HandlersRegistry


runner_handlers_registry = HandlersRegistry()


@runner_handlers_registry.register()
async def run_code():
    pass
