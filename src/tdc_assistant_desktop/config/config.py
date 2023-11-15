from typing import Final, TypedDict


class Config(TypedDict):
    LOG: bool
    DELAY_AFTER_OPTION_SELECT_IN_SECONDS: float


config: Final[Config] = {"LOG": True, "DELAY_AFTER_OPTION_SELECT_IN_SECONDS": 2.5}
