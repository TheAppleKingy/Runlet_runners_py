from typing import Protocol, Literal


class DockerServiceInterface(Protocol):
    def build(self, for_lang: str): ...
