from source.StaticMethods import StaticMethods
from Config import Config
from source.JSONWorker import JSONWorker
import hues

import time


class TimeHandler:
    def __init__(self, botapi):
        self.botapi = botapi

    def time_controller(self):
        catched = False
        if not Config.workout_time:
            return True
        while True:
            if int(StaticMethods.get_time().strftime('%H')) not in range(Config.workout_time[0],
                                                                         Config.workout_time[1] + 1):
                if not catched:
                    catched = True
                    self.botapi.write_msg(
                        'Подготовка ко сну. Следующие посты будут доступны с {}'.format(Config.workout_time[0]),
                        JSONWorker.read_json('nonekey.json'))
                    hues.warn('Going to sleep up to {}'.format(Config.workout_time[0]))
                time.sleep(3600 - int(StaticMethods.get_time().strftime('%M')) * 60)

            else:
                break
        return True
