from typing import Protocol


class CodeRunnerInterface(Protocol):
    def run_code(self, for_lang: str, input_path: str, cases_count: int) -> str: ...
