from datetime import datetime


from utils.constants import DATETIME_FORMAT


class BaseObserver:
    def _log(self, message: str, dt: datetime):
        print(
            "[{}] {:40s} ({})".format(
                self.__class__.__name__,
                message,
                dt.strftime(DATETIME_FORMAT),
            )
        )
