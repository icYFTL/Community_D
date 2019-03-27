import sys
import time
from ConsoleWorker import ConsoleWorker


class Preview(object):
    def do():
        CLSWork = ConsoleWorker()
        CLSWork.ClearConsole()
        print('[CommD] v1.3 Beta Release')
        corp = 'by icYFTL\n\n'

        notice = "If you got error or smth else: write me\nTelegram: @icYFTL\nDarkWeb: icyFTL"

        for i in range(len(corp)):
            if corp[i].isalpha() or corp[i - 1].isalpha() and i != 0:
                sys.stdout.write(corp[i])
                sys.stdout.flush()
                time.sleep(0.2)
            else:
                sys.stdout.write(corp[i])
                sys.stdout.flush()
        print(notice + "\n\n\n")
