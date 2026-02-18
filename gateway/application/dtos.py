from typing import Literal

from pydantic import BaseModel


class TestSolutionDTO(BaseModel):
    student_id: int
    problem_id: int
    lang: Literal[
        "py",
        "go",
        "js",
        "cpp",
        "cs"
    ]
    code: str
