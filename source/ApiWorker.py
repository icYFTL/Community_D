from source.BotApi import BotApi
from source.ImageHandler import ImageHandler
from source.TimeHandler import TimeHandler
from source.UserApi import UserApi
from source.UsedIdsController import UsedIdsController
import hues

import os
import requests
from PIL import Image
import time


class ApiWorker:
    def __init__(self, token, token_c):
        self.token = token  # User's vk api token
        self.commtoken = token_c  # Community's vk api token
        self.botapi = BotApi(self.commtoken)  # Class which works with community's api
        self.User = UserApi(token)  # Class which works with user's api
        self.time_handler = TimeHandler(self.botapi)  # Class which looking for current time
        self.usedids = UsedIdsController.read()  # Getting usedids from file
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

        if posts is False:  # If there're no posts found
            if self.time_handler.time_controller() is False:  # If day
                hues.log('Posts not found. Will retry in 1 hour')
                self.botapi.write_msg('Постов нема. Попробую поискать их еще раз через 1 час.', None)
                time.sleep(3600)  # if there're no posts -> sleep 1 hour
                return False
        hues.log('"GroupsChecker" has been done.')
        return posts

    def parse_data(self):
        '''
        Parsing data from posts.
        This function gets text and attachment from 1 post.
        '''

        hues.log('Parsing data has been started.')

        posts = self.groups_checker()  # Getting posts
        while posts is False:  # While posts not found
            hues.warn('Error while post getting. Retrying...')
            posts = self.groups_checker()

        text = None
        attachment = None

        for i in posts:
            text = self.get_text(i)
            attachment = self.get_photo(i)

            if not text or not attachment:
                continue
            break
        if text:
            if attachment:
                pass
            else:
                attachment = None
        else:
            text = None

        hues.log('Got photo and text.')
        return [text, attachment]

    def get_text(self, data):
        data = data.get('text')
        if len(data) < 1:
            return False
        return data

    def get_photo(self, data):
        attachment = None
        try:
            if str(data.get('from_id')) + '_' + str(
                    data.get('id')) in self.usedids:  # Checking ID of post in used IDs
                return False
            attachment = data.get('attachments')
            self.usedids.append(
                '{}_{}'.format(str(data.get('from_id')), str(data.get('id'))))  # Mark current post as used
            UsedIdsController.write('{}_{}'.format(str(data.get('from_id')), str(data.get('id'))))
        except:
            return False
        if attachment:
            for j in attachment:  # Looking for highest size of picture
                if j.get('type') == 'photo':
                    attachment = j.get('photo').get('sizes')[-1].get('url')
                    return attachment
        else:
            hues.warn('I can\'t resolve photo.\nRetrying...')
            return False
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

        while data is False:
            hues.warn('Error while parsing. Retrying...')
            data = self.parse_data()

        try:
            os.mkdir('./source/tmp/')
        except:
            pass

            f = open('source/tmp/img.jpg', 'wb')
            try:
                f.write(requests.get(data[1]).content)
            except:
                hues.warn('Bad request.\nFunction will be restarted.')
                f.close()
                return False

            f.close()
            hues.log('Got photo.')

            ## WATERMARK LANDING ##

            img = Image.open("./source/tmp/img.jpg")
            watermark = Image.open("./source/waterx.png")

            result = ImageHandler.add_watermark(img, watermark)
            result.save('./source/tmp/result.png')

            os.remove('source/tmp/img.jpg')
            hues.log('Watermark landing done.')

            ## IMAGE UPLOADING ##

            image = self.User.image_upload()
            if image is False:
                image = None

            data = [data[0], image]
            os.remove('./source/tmp/result.png')
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
