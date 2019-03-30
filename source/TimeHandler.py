from StaticMethods import StaticMethods
from Config import StaticData

import time


class TimeHandler:
    def __init__(self, botapi):
        self.botapi = botapi

    def time_controller(self):
        catched = False
        if not StaticData.workout_time:
            return True
        while True:
            if int(StaticMethods.get_time().strftime('%H')) not in range(StaticData.workout_time[0],
                                                                         StaticData.workout_time[1] + 1):
                time.sleep(3600 + int(StaticMethods.get_time().strftime('%H')) * 60)
                if not catched:
                    self.botapi.write_msg(
                        'Подготовка ко сну. Следующие посты будут доступны с {}'.format(StaticData.workout_time[0]),
                        None)
            else:
                break
        return True
