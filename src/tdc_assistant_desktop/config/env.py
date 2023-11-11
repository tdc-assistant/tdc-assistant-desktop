from typing import TypedDict, Literal, Optional, Union

import os
from os.path import join, dirname
from dotenv import load_dotenv


class EnvironmentVariables(TypedDict):
    FIRST_NAME: Optional[str]
    LAST_INITIAL: Optional[str]
    TDC_ASSISTANT_URL: Optional[str]


dotenv_path = join(dirname(__file__), "..", "..", "..", ".env")
load_dotenv(dotenv_path)

EnvironmentVariableKey = Union[
    Literal["FIRST_NAME"],
    Literal["LAST_INITIAL"],
    Literal["TDC_ASSISTANT_URL"],
]

env: dict[EnvironmentVariableKey, str] = {
    "FIRST_NAME": "",
    "LAST_INITIAL": "",
    "TDC_ASSISTANT_URL": "",
}

for env_key in env:
    env_val = os.environ.get(env_key)
    if env_val is None:
        raise Exception(f"Cannot find environment variable: '{env_key}'")
    env[env_key] = env_val
