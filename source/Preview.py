import sys
import time
from source.ConsoleWorker import ConsoleWorker
from source.StaticData import StaticData


class Preview:
    @staticmethod
    def do():
        CLSWork = ConsoleWorker()
        CLSWork.ClearConsole()
        print('[CommD] v{} Stable Alpha Release'.format(StaticData.version))
        corp = 'by icYFTL\n\n'

        notice = "If you got error or smth else: write me\nTelegram: @icYFTL\nDarkWeb: Denuvo"

        for i in range(len(corp)):
            if corp[i].isalpha() or corp[i - 1].isalpha() and i != 0:
                sys.stdout.write(corp[i])
                sys.stdout.flush()
                time.sleep(0.2)
            else:
                sys.stdout.write(corp[i])
                sys.stdout.flush()
        print(notice + "\n\n\n")
