import sys

sys.path.append('./source/exceptions/')

from BotApi import BotApi
from ImageHandler import ImageHandler
from TimeHandler import TimeHandler
from UserApi import UserApi

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
        self.usedids = []  # Used IDs of posts

    def groups_checker(self):
        '''
        Checking groups in StaticData.groups for posts.
        Function gets only fresh posts (with current date posted)
        '''

        self.time_handler.time_controller()  # Checking for times of day

        print('Started "GroupsChecker"')

        posts = self.User.posts_checker()  # Getting posts

        if posts is False:  # If there're no posts found
            if self.time_handler.time_controller() is False:  # If day
                print('Posts not found. Will retry in 1 hour')
                self.botapi.write_msg('Постов нема. Попробую поискать их еще раз через 1 час.', None)
                time.sleep(3600)
                return False
        print('"GroupsChecker" has been done.')
        return posts

    def parse_data(self):
        '''
        Parsing data from posts.
        This function gets text and attachment from 1 post.
        '''

        print('Parsing data has been started.')

        posts = self.groups_checker()  # Getting posts
        while posts is False:  # While posts not found
            print('Error while post getting. Retrying...')
            posts = self.groups_checker()

        text = None
        attachment = None

        for i in posts:
            if attachment is None:
                try:
                    if i.get('id') in self.usedids:  # Checking ID of post in used IDs
                        continue
                    text = i.get('text')  # Getting text from post
                    if len(text) < 1:
                        text = None
                    attachment = i.get('attachments')
                    self.usedids.append(i.get('id'))  # Mark current post as used
                except:
                    continue
                if attachment:
                    for j in attachment:  # Looking for highest size of picture
                        if j.get('type') == 'photo':
                            attachment = j.get('photo').get('sizes')[-1].get('url')
                            break
            else:
                break

            if attachment is None:
                print('I can\'t resolve photo.\nRetrying...')
                return False

        print('Got photo and text.')
        return [text, attachment]

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
        print('Preparing for post has been initiated.')

        data = self.parse_data()

        while data is False:
            print('Error while parsing. Retrying...')
            data = self.parse_data()

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
                return False

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

            image = self.User.image_upload()
            while image is False:
                image = self.User.image_upload()

            data = [data[0], ]
            os.remove('./source/tmp/result.png')
            print('Image uploaded.')

            ## ACCEPTABLE MESSAGE SENDING

            self.botapi.write_msg(data[0], data[1])
            time.sleep(0.4)
            self.botapi.write_msg('Сделать пост?\n1 - Запостить\n2 - Обновить', None)

            print('Messages sent.')

            ## WAIT FOR CALLBACK

            while True:
                repl = self.botapi.message_handler()
                username = self.User.get_user(repl[1])
                if repl[0] == '1':

                    self.User.post(data[0], data[1])
                    self.botapi.write_msg('Предыдущий пост был принят администратором {}'.format(username), None)
                    break

                elif repl[0] == '2':

                    self.botapi.write_msg('Предыдущий пост был отклонен администратором {}'.format(username), None)
                    return False

                else:
                    self.botapi.write_msg('Напишите 1 или 2', None)
                    continue

    def post(self):  # Posting
        self.before_post()
