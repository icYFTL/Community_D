class JSONWorker:
    @staticmethod
    def read_json(file):
        return open("source/keyboards/{}".format(file), "r", encoding="UTF-8").read()
