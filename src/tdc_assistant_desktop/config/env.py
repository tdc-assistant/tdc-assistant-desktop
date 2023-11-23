from typing import TypedDict, Literal, Optional, Union

import os
from os.path import join, dirname
from dotenv import load_dotenv


class EnvironmentVariables(TypedDict):
    FIRST_NAME: Optional[str]
    LAST_INITIAL: Optional[str]
    TDC_ASSISTANT_URL: Optional[str]
    PUBLIC_CHAT_POP_OUT_COORDS: Optional[tuple[int, int]]
    PUBLIC_CHAT_TEXT_AREA_CORDS: Optional[tuple[int, int]]
    INSERT_CODE_EDITOR_COORD_PATH: Optional[list[tuple[int, int]]]


dotenv_path = join(dirname(__file__), "..", "..", "..", ".env")
load_dotenv(dotenv_path)

EnvironmentVariableKey = Union[
    Literal["FIRST_NAME"],
    Literal["LAST_INITIAL"],
    Literal["TDC_ASSISTANT_URL"],
    Literal["PUBLIC_CHAT_POP_OUT_COORDS"],
    Literal["PUBLIC_CHAT_TEXT_AREA_COORDS"],
    Literal["INSERT_CODE_EDITOR_COORD_PATH"],
    Literal["AWS_ACCESS_KEY_ID"],
    Literal["AWS_SECRET_ACCESS_KEY"],
    Literal["REGION"],
    Literal["BUCKET_NAME"],
    Literal["OBJECT_URL_DOMAIN"],
]

env: dict[
    EnvironmentVariableKey, Union[bool, str, tuple[int, int], list[tuple[int, int]]]
] = {
    "FIRST_NAME": "",
    "LAST_INITIAL": "",
    "TDC_ASSISTANT_URL": "",
    "PUBLIC_CHAT_POP_OUT_COORDS": (0, 0),
    "PUBLIC_CHAT_TEXT_AREA_COORDS": (0, 0),
    "INSERT_CODE_EDITOR_COORD_PATH": [(0, 0), (0, 0), (0, 0), (0, 0)],
    "AWS_ACCESS_KEY_ID": "",
    "AWS_SECRET_ACCESS_KEY": "",
    "REGION": "",
    "BUCKET_NAME": "",
    "OBJECT_URL_DOMAIN": "",
}

for env_key in env:
    env_val = os.environ.get(env_key)
    if env_val is None:
        raise Exception(f"Cannot find environment variable: '{env_key}'")
    elif env_key.endswith("COORDS"):
        x, y = map(int, env_val.split(","))
        env[env_key] = x, y
    elif env_key.endswith("PATH"):
        path: list[tuple[int, int]] = []
        for coord in env_val.split(" "):
            x, y = map(int, coord.split(","))
            path.append((x, y))
        env[env_key] = path
    else:
        env[env_key] = env_val
