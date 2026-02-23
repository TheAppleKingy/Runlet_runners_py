from typing import Protocol

from gateway.domain.types import CodeName


class CodeRunnerInterface(Protocol):
    def run_code(self, for_lang: CodeName, input_path: str, cases_count: int) -> str: ...
