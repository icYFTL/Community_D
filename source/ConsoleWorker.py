import os


class ConsoleWorker:
    @staticmethod
    def ClearConsole():
        if os.system('clear') != 0:
            os.system('cls')
