from typing import Final, TypedDict


class Config(TypedDict):
    LOG: bool


config: Final[Config] = {"LOG": True}
