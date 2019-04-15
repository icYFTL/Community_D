import os


class UsedIdsController(object):
    def directory():
        if os.path.exists('./data/'):
            return True
        else:
            try:
                os.mkdir('./data/')
            except:
                return False
        return True

    def write(id):
        if not UsedIdsController.directory():
            print('Something went wrong with permissions.')
            exit()
        try:
            f = open('./data/used.txt', 'a')
            f.write(str(id) + '\n')
            f.close()
        except:
            return False
        return True

    def read():
        if not UsedIdsController.directory():
            print('Something went wrong with permissions.')
            exit()
        try:
            f = open('./data/used.txt', 'r')
            data = f.read().split('\n')
            f.close()
            return data
        except:
            return []
