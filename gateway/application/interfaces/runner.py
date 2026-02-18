from typing import Protocol


class CodeRunnerInterface(Protocol):
    def __init__(self, docker_cli):
        super().__init__()
