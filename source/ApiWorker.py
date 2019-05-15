from source.BotApi import BotApi
from source.ImageHandler import ImageHandler
from source.TimeHandler import TimeHandler
from source.UserApi import UserApi
from source.BDWorker import BDWorker
from source.StaticMethods import StaticMethods
from source.StaticData import StaticData
import hues

import os
import requests
import time


class ApiWorker:
    def __init__(self, token, token_c):
        self.token = token  # User's vk api token
        self.commtoken = token_c  # Community's vk api token
        self.botapi = BotApi(self.commtoken)  # Class which works with community's api
        self.User = UserApi(token)  # Class which works with user's api
        self.time_handler = TimeHandler(self.botapi)  # Class which looking for current time
        self.bdworker = BDWorker()
        self.initializator()

    def initializator(self):
        self.botapi.write_msg('Скрипт был запущен.', None)
        hues.success('Script has been started')

    def groups_checker(self):
        '''
        Checking groups in Config.groups for posts.
        Function gets only fresh posts (with current date posted)
        '''

        self.time_handler.time_controller()  # Checking for times of day

        hues.log('Started "GroupsChecker"')

        posts = self.User.posts_checker()  # Getting posts

        while not posts:  # If there're no posts found
            if self.time_handler.time_controller():
                hues.warn('Posts not found. Will retry in 1 hour')
                self.botapi.write_msg('Постов нема. Попробую поискать их еще раз через 1 час.', None)
                time.sleep(3600)  # if there're no posts -> sleep 1 hour
                posts = self.User.posts_checker()
        true_posts = []
        for i in range(len(posts)):
            attachment = self.get_photo(posts[i])
            if self.bdworker.getter(post_id=posts[i].get('id'),
                                    group_id=posts[i].get('from_id')) or self.bdworker.check_photo(attachment):
                continue
            if not attachment:
                continue
            true_posts.append(posts[i])
        hues.log('"GroupsChecker" has been done.')
        return [true_posts, StaticMethods.get_time().strftime('%d/%m/%y')]

    def parse_data(self):
        '''
        Parsing data from posts.
        This function gets text and attachment from 1 post.
        '''

        hues.log('Parsing data has been started.')

        try:
            if not StaticData.posts[0] or StaticData.posts[1] != StaticMethods.get_time().strftime('%d/%m/%y'):
                StaticData.posts = self.groups_checker()  # Getting posts
        except IndexError:
            StaticData.posts = self.groups_checker()

        text = None
        attachment = None
        post_iter = None

        for i in range(len(StaticData.posts[0])):
            text = self.get_text(StaticData.posts[0][i])
            attachment = self.get_photo(StaticData.posts[0][i])

            self.bdworker.add_post(post_id=StaticData.posts[0][i].get('id'),
                                   post_date=StaticMethods.get_time().strftime('%d/%m/%y %H:%M:%S'),
                                   group_id=StaticData.posts[0][i].get('from_id'),
                                   photo_md5=StaticMethods.get_md5(attachment))
            post_iter = i
            break

        try:
            del StaticData.posts[0][post_iter]
        except TypeError:
            return False
        hues.log('Got photo and text.')
        return [text, attachment]

    def get_text(self, data):
        data = data.get('text')
        if len(data) < 1:
            return False
        return data

    def get_photo(self, data):
        attachment = data.get('attachments')
        if attachment:
            for j in attachment:  # Looking for highest size of picture
                if j.get('type') == 'photo':
                    attachment = j.get('photo').get('sizes')[-1].get('url')
                    return requests.get(attachment).content
        else:
            hues.warn('I can\'t resolve photo.\nRetrying...')
        return False

    def before_post(self):
        '''
        Preparing for post:
            • Saving photo on local
            • Adding watermark on photo
            • Image uploading to vk server
            • Deleting photo
            • Accepting messages sending
            • Messages handling
        '''
        hues.log('Preparing for post has been initiated.')

        data = self.parse_data()
        while not data:
            data = self.parse_data()

        try:
            os.mkdir('./source/tmp/')
        except:
            pass

        f = open('source/tmp/img.jpg', 'wb')
        f.write(data[1])
        f.close()
        hues.log('Photo was downloaded.')

        ## WATERMARK LANDING ##

        ImageHandler.watermark_with_transparency('source/tmp/img.jpg')

        os.remove('source/tmp/img.jpg')
        hues.log('Watermark landing done.')

        ## IMAGE UPLOADING ##

        image = self.User.image_upload()
        if image is False:
            image = None

        data = [data[0], image]
        os.remove('./source/tmp/result.jpg')
        hues.log('Image uploaded.')

        ## ACCEPTABLE MESSAGE SENDING

        self.botapi.write_msg(data[0], data[1])
        time.sleep(0.4)
        self.botapi.write_msg('Сделать пост?\n1 - Запостить\n2 - Следующий пост',
                              None)

        hues.log('Messages sent.')

        ## WAITING FOR CALLBACK

        while True:
            repl = self.botapi.message_handler()
            username = self.User.get_user(repl[2])
            if repl[0] == '1':

                self.User.post(data[0], data[1])
                self.botapi.write_msg('Предыдущий пост был принят пользователем {}'.format(username), None)
                break

            elif repl[0] == '2':

                self.botapi.write_msg('Предыдущий пост был отклонен пользователем {}'.format(username), None)
                return False
            else:
                self.botapi.write_msg('Напишите 1 или 2', None)
                continue

    def post(self):  # Posting
        self.before_post()
