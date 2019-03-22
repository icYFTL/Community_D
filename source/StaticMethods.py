import pytz
from datetime import datetime


class StaticMethods(object):
    def get_time():
        return datetime.now(pytz.timezone('Europe/Moscow'))
