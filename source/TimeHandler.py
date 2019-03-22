import sys

sys.path.append('./source/')

from StaticMethods import StaticMethods

import time


class TimeHandler:
    def __init__(self, botapi):
        self.botapi = botapi

    def time_controller(self):
        night = ['23', '00', '01', '02', '03', '04', '05', '06', '07', '08', '09']
        current_time = StaticMethods.get_time().strftime('%H,%M')
        current_time = current_time.split(',')
        if current_time[0] in night:
            self.botapi.write_msg('Поготовка к ночи. Постинг будет доступен с 11 утра.', None)
            print('\nPreparing for global sleep...')
            if current_time[0] == '23':
                time.sleep(43200 - int(current_time[1]) * 60)
            elif current_time[0] == '00':
                time.sleep(39600 - int(current_time[1]) * 60)
            elif current_time[0] == '01':
                time.sleep(36000 - int(current_time[1]) * 60)
            elif current_time[0] == '02':
                time.sleep(32400 - int(current_time[1]) * 60)
            elif current_time[0] == '03':
                time.sleep(28800 - int(current_time[1]) * 60)
            elif current_time[0] == '04':
                time.sleep(25200 - int(current_time[1]) * 60)
            elif current_time[0] == '05':
                time.sleep(21600 - int(current_time[1]) * 60)
            elif current_time[0] == '06':
                time.sleep(18000 - int(current_time[1]) * 60)
            elif current_time[0] == '07':
                time.sleep(14400 - int(current_time[1]) * 60)
            elif current_time[0] == '08':
                time.sleep(10800 - int(current_time[1]) * 60)
            elif current_time[0] == '09':
                time.sleep(7200 - int(current_time[1]) * 60)
            elif current_time[0] == '10':
                time.sleep(3600 - int(current_time[1]) * 60)
            else:
                return False
        return True
