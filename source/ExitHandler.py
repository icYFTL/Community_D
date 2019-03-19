import os


class ExitHandler(object):
    def bye():
        print('Shutting down...')

        try:
            os.remove('source/tmp/img.jpg')
        except:
            pass

        try:
            os.remove('./source/tmp/result.png')
        except:
            pass

        try:
            os.removedirs('./source/tmp/')
        except:
            pass
