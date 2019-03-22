import pytz
from datetime import datetime
import time


class TimeHandler:
    def __init__(self, botapi):
        self.botapi = botapi

    def get_time(self):
        return datetime.now(pytz.timezone('Europe/Moscow'))

    def time_controller(self):
        night = ['23', '00', '01', '02', '03', '04', '05', '06', '07', '08', '09']
        current_time = self.get_time().strftime('%H')
        if current_time in night:
            self.botapi.write_msg('Поготовка к ночи. Постинг будет доступен с 11 утра.', None)
            print('\nPreparing for global sleep...')
            if current_time == '23':
                time.sleep(39600 + int(self.get_time().strftime('%M')) * 60)
            elif current_time == '00':
                time.sleep(36000 + int(self.get_time().strftime('%M')) * 60)
            elif current_time == '01':
                time.sleep(32400 + int(self.get_time().strftime('%M')) * 60)
            elif current_time == '02':
                time.sleep(28800 + int(self.get_time().strftime('%M')) * 60)
            elif current_time == '03':
                time.sleep(25200 + int(self.get_time().strftime('%M')) * 60)
            elif current_time == '04':
                time.sleep(21600 + int(self.get_time().strftime('%M')) * 60)
            elif current_time == '05':
                time.sleep(18000 + int(self.get_time().strftime('%M')) * 60)
            elif current_time == '06':
                time.sleep(14400 + int(self.get_time().strftime('%M')) * 60)
            elif current_time == '07':
                time.sleep(10800 + int(self.get_time().strftime('%M')) * 60)
            elif current_time == '08':
                time.sleep(7200 + int(self.get_time().strftime('%M')) * 60)
            elif current_time == '09':
                time.sleep(3600 + int(self.get_time().strftime('%M')) * 60)
            else:
                return False
        return True
