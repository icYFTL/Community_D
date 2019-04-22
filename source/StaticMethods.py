import pytz
from datetime import datetime


class StaticMethods:
    @staticmethod
    def get_time():
        return datetime.now(pytz.timezone('Europe/Moscow'))
