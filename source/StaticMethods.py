import pytz
from datetime import datetime
import hashlib


class StaticMethods:
    @staticmethod
    def get_time():
        return datetime.now(pytz.timezone('Europe/Moscow'))

    @staticmethod
    def get_md5(data):
        return hashlib.md5(str(data).encode("utf-8")).hexdigest()
