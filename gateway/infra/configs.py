import re

from typing import Literal

from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings


class RedisConfig(BaseSettings):
    redis_password: str
    redis_host: str

    @property
    def conn_url(self):
        return f"redis://:{self.redis_password}@{self.redis_host}:6379"


LangCode = Literal["py", "js", "go", "cs", "cpp"]


class LangRunnerResourseInfo(BaseModel):
    image: str
    mem_limit: str
    cpu_cores: float
    envs: list[str] = Field(default_factory=list)
    compile_args: list[str]
    run_args: list[str]
    run_timeout: int


class RunnersConfig(BaseModel):
    runners: dict[LangCode, LangRunnerResourseInfo]
    dockerfiles_path: str
    runner_dockerfile_name: str
    runner_image_name_pattern: str
    shared_image_name: str
    shared_dockerfile_name: str
    context_path: str
    src_placeholder: str
    bin_placeholder: str

    @field_validator("runners", mode="after")
    @classmethod
    def validate_runners(cls, value: dict[str, LangRunnerResourseInfo]):
        for code in LangCode.__args__:
            if code not in value:
                raise KeyError(f"Have to define config for '{code}' runner")
        return value
