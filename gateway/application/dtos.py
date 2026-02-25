from typing import Literal, TypedDict

from pydantic import BaseModel, Field

from gateway.domain.types import CodeName


class TestCaseDTO(BaseModel):
    test_num: int
    input: str
    output: str


class RunDataDTO(BaseModel):
    test_num: int
    input: str


class TestSolutionDTO(BaseModel):
    student_id: int
    problem_id: int
    course_id: int
    lang: CodeName
    code: str
    run_data: list[RunDataDTO] = Field(min_length=1)


class DictRunData(TypedDict):
    test_num: int
    input: str


class DictTestSolutionDTO(TypedDict):
    student_id: int
    problem_id: int
    course_id: int
    lang: CodeName
    code: str
    run_data: list[DictRunData]


class InputDTO(BaseModel):
    code: str
    run_data: list[RunDataDTO]


class ResultDTO(BaseModel):
    test_cases: list[TestCaseDTO]
    err_msg: str
    code: str = ""
    problem_id: int = 0
    student_id: int = 0
    course_id: int = 0
