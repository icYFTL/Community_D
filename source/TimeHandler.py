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
        for i in range(StaticData.workout_time[0] + 1, StaticData.workout_time[1]):
            while StaticMethods.get_time().strftime('%H') == i:
                if catched is False:
                    catched = True
                    self.botapi.write_msg(
                        'Подготовка ко сну. Следующие посты будут доступны с {} часов.'.format(
                            StaticData.workout_time[0]), None)
                    print('Preparing for night.')
                time.sleep(10)
        return True
