import sys

sys.path.append('./source/exceptions/')

from VkApiException import VkApiException
from BotApi import BotApi
from ImageHandler import ImageHandler
from StaticData import StaticData
from TimeHandler import TimeHandler

import vk
import random
import os
import requests
from PIL import Image
from datetime import datetime
import time


class ApiWorker:
    def __init__(self, token, token_c):
        self.token = token
        self.commtoken = token_c
        self.vk_api = None
        self.vk_api_c = None
        self.get_session()
        self.usedids = []
        self.community_long_poll = None
        self.available_posts = []
        self.botapi = BotApi(self.commtoken)
        self.time_handler = TimeHandler(self.botapi)

    def get_session(self):
        try:
            print('Getting sessions...')

            session = vk.Session(access_token=self.token)
            self.vk_api = vk.API(session, v='5.74')

            print('Got session for user.')

        except:
            raise VkApiException

    def groups_checker(self):
        self.time_handler.time_controller()

        print('Started "GroupsChecker"')
        current_date = self.time_handler.get_time().strftime('%Y-%m-%d').split('-')

        for i in StaticData.groups:
            posts = self.vk_api.wall.get(owner_id=int(i),
                                         count=20, offset=0)
            for j in range(len(posts.get('items'))):
                post_date = datetime.utcfromtimestamp(int(posts.get('items')[j].get('date'))).strftime(
                    '%Y-%m-%d').split('-')
                if post_date == current_date:
                    self.available_posts.append(posts.get('items')[j])
            time.sleep(0.4)
        print('"GroupsChecker" has been terminated.')

        if self.available_posts is []:
            if self.time_handler.time_controller() is False:
                self.botapi.write_msg('Посты кончились. Попробую на наличие новых через час.', None)
                return False
        return True

    def parse_data(self):
        print('Parsing data has been started.')
        if self.groups_checker() is False:
            time.sleep(3600)
            return
        text = None
        attachment = None
        for i in self.available_posts:
            attachment_m = None
            try:
                if i.get('id') in self.usedids:
                    continue
                text = i.get('text')
                attachment_m = i.get('attachments')
                self.usedids.append(i.get('id'))
            except:
                continue
            for j in attachment_m:
                if j.get('type') == 'photo':

                    if '2560' in str(j):
                        attachment = j.get('photo').get('photo_2560')
                    elif '1280' in str(j):
                        attachment = j.get('photo').get('photo_1280')
                    elif '807' in str(j):
                        attachment = j.get('photo').get('photo_807')
                    else:
                        attachment = None
                        print('I can\'t resolve photo.\nRetrying...')
                        return
            print('Got photo and text.')
            return [text, attachment]

    def before_post(self):
        print('Preparing for post has been initiated.')
        data = self.parse_data()

        while data is None:
            data = self.parse_data()
            time.sleep(1)

        while data[0] is None or data[1] is None:
            data = self.parse_data()
            time.sleep(1)

        try:
            os.mkdir('./source/tmp/')
        except:
            pass

            f = open('source/tmp/img.jpg', 'wb')
            try:
                f.write(requests.get(data[1]).content)
            except requests.exceptions.MissingSchema:
                print('Bad request.\nFunction will be restarted.')
                f.close()
                time.sleep(1)
                return

            f.close()
            print('Got photo.')

            ## WATERMARK LANDING ##

            img = Image.open("./source/tmp/img.jpg")
            watermark = Image.open("./source/waterx.png")

            result = ImageHandler.add_watermark(img, watermark)
            result.save('./source/tmp/result.png')

            os.remove('source/tmp/img.jpg')
            print('Watermark landing done.')

            ## IMAGE UPLOADING ##

            upload_server = self.vk_api.photos.getWallUploadServer(group_id=99558704)
            temp_photo = requests.post(upload_server['upload_url'],
                                       files={'photo': open('source/tmp/result.png', 'rb')}).json()
            save_method = \
                self.vk_api.photos.saveWallPhoto(group_id=99558704, photo=temp_photo['photo'],
                                                 server=temp_photo['server'],
                                                 hash=temp_photo['hash'])[0]
            output = 'photo{}_{}'.format(save_method['owner_id'], save_method['id'])
            data = [data[0], output]
            os.remove('./source/tmp/result.png')
            print('Image uploaded.')

            ## ACCEPTABLE MESSAGE SENDING

            self.botapi.write_msg(data[0], data[1])
            time.sleep(0.5)
            self.botapi.write_msg('Сделать пост?\n1 - Запостить\n2 - Показать следующий пост')

            print('Messages sent.')

            ## WAIT FOR CALLBACK

            repl = self.botapi.message_handler()

            if repl == '1':

                self.botapi.write_msg('Предыдущий пост был принят.', None)

            elif repl == '2':

                self.botapi.write_msg('Предыдущий пост был отклонен.')
                return False

            print('Preparing done.')
            return data

    def post(self):
        data = self.before_post()

        if data is False:
            self.post()
            print('\n\n\n\n')
            return
        if data is None:
            return False
        self.vk_api.wall.post(owner_id=-99558704, message=data[0], attachments=data[1])
