import sys

sys.path.append('./source/exceptions/')

from VkApiException import VkApiException

import vk
import random
import os
import requests
from ImageHandler import ImageHandler
from PIL import Image
from StaticData import StaticData
from datetime import datetime
import time
import pytz


class ApiWorker:
    def __init__(self, token, token_c):
        self.token = token
        self.commtoken = token_c
        self.vk_api = None
        self.vk_api_c = None
        self.get_session()
        self.usedids = []
        self.community_long_poll = None
        self.available_groups = []

    def get_long_poll(self):
        self.community_long_poll = self.vk_api_c.messages.getLongPollServer(need_pts=1)

    def get_time(self):
        return datetime.now(pytz.timezone('Europe/Moscow'))

    def message_send(self, message):
        for i in StaticData.admins:
            self.vk_api_c.messages.send(user_id=i,
                                        message=message,
                                        random_id=random.randint(0, 10000))

    def time_controller(self):
        night = ['23', '00', '01', '02', '03', '04', '05', '06', '07', '08', '09']
        current_time = self.get_time().strftime('%H')
        if current_time in night:
            self.message_send('Preparing for night.\nThe next posts will be available in 10 AM.')
            print('\nPreparing for global sleep...')
            if current_time == '23':
                time.sleep(39600 + int(self.get_time().strftime('%M')) * 60)
            elif current_time == '00':
                time.sleep(36000 + int(self.get_time().strftime('%M')) * 60)
            elif current_time == '01':
                time.sleep(32400 + int(self.get_time().strftime('%M')) * 60)
            elif current_time == '02':
                time.sleep(28800 + int(self.get_time().strftime('%M')) * 60)
            elif current_time == '03':
                time.sleep(25200 + int(self.get_time().strftime('%M')) * 60)
            elif current_time == '04':
                time.sleep(21600 + int(self.get_time().strftime('%M')) * 60)
            elif current_time == '05':
                time.sleep(18000 + int(self.get_time().strftime('%M')) * 60)
            elif current_time == '06':
                time.sleep(14400 + int(self.get_time().strftime('%M')) * 60)
            elif current_time == '07':
                time.sleep(10800 + int(self.get_time().strftime('%M')) * 60)
            elif current_time == '08':
                time.sleep(7200 + int(self.get_time().strftime('%M')) * 60)
            elif current_time == '09':
                time.sleep(3600 + int(self.get_time().strftime('%M')) * 60)
            else:
                return False
        return True

    def get_session(self):
        try:
            print('Getting sessions...')

            session = vk.Session(access_token=self.token)
            self.vk_api = vk.API(session, v='5.74')

            print('Got session for user.')

            commsession = vk.Session(access_token=self.commtoken)
            self.vk_api_c = vk.API(commsession, v='5.92')

            print('Got session for community.')

        except:
            raise VkApiException

    def groups_checker(self):
        self.time_controller()
        print('Started "GroupsChecker"')
        current_date = self.get_time().strftime('%Y-%m-%d').split('-')
        for i in StaticData.groups:
            posts = self.vk_api.wall.get(owner_id=int(i),
                                         count=20, offset=0)
            for j in range(len(posts.get('items'))):
                post_date = datetime.utcfromtimestamp(int(posts.get('items')[j].get('date'))).strftime(
                    '%Y-%m-%d').split('-')
                if post_date == current_date:
                    self.available_groups.append(posts.get('items')[j])
            time.sleep(0.4)
        print('"GroupsChecker" has been terminated.')
        if self.available_groups is []:
            if self.time_controller() is False:
                self.message_send('Unfortunately, the posts ended. Will retry in 1 hour')
                return False


    def parse_data(self):
        print('Parsing data has been started.')
        if self.groups_checker() is False:
            time.sleep(3600)
            self.post()
            return
        text = None
        attachment = None
        for i in self.available_groups:
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
                self.before_post()
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

            for i in StaticData.admins:
                self.vk_api_c.messages.send(user_id=i, message=data[0],
                                            attachment="photo" + str(save_method['owner_id']) + "_" + str(
                                                save_method['id']) + "_" +
                                                       str(save_method['access_key']),
                                            random_id=random.randint(0, 10000))
                time.sleep(0.5)
                self.vk_api_c.messages.send(user_id=i,
                                            message="Accept post?\nYou can:\n1 - Accept\n2 - Show next",
                                            random_id=random.randint(0, 10000))
                time.sleep(0.5)
            self.get_long_poll()
            print('Messages sent.')

            ## WAIT FOR CALLBACK

            while True:
                try:
                    repl = self.vk_api_c.messages.getLongPollHistory(ts=self.community_long_poll['ts'],
                                                                     pts=self.community_long_poll['pts'])
                    sender = repl.get('messages').get('items')[0].get('from_id')
                    if sender not in StaticData.admins:
                        self.get_long_poll()
                        continue
                    sender = self.vk_api.users.get(user_ids=sender)
                    sender = '{} {}'.format(sender[0].get('first_name'), sender[0].get('last_name'))

                    repl = repl.get('messages').get('items')[0].get('text')

                    print('Got repl: {}'.format(repl))

                    self.get_long_poll()
                    print('Long poll restarted.')

                    if repl == '1':
                        for i in StaticData.admins:
                            self.vk_api_c.messages.send(user_id=i,
                                                        message="Previous post has been accepted by {}".format(sender),
                                                        random_id=random.randint(0, 10000))
                        break
                    if repl == '2':
                        for i in StaticData.admins:
                            self.vk_api_c.messages.send(user_id=i,
                                                        message="Previous post has been declined by {}".format(sender),
                                                        random_id=random.randint(0, 10000))
                        return False
                    time.sleep(1)
                except IndexError:
                    print('Waiting for message...')
                    time.sleep(1)
                    continue
                except Exception as e:
                    print(str(e))
                    self.get_long_poll()
                    continue
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
        for i in StaticData.admins:
            self.vk_api_c.messages.send(user_id=i,
                                        message="The next post will be offered in 1 hour.\nWanna post now?\n1 - Yes\n2 - Not now",
                                        random_id=random.randint(0, 10000))
            print('Posted.\n\n\n\n')
            while True:
                try:
                    repl = self.vk_api_c.messages.getLongPollHistory(ts=self.community_long_poll['ts'],
                                                                     pts=self.community_long_poll['pts'])
                    sender = repl.get('messages').get('items')[0].get('from_id')
                    if sender not in StaticData.admins:
                        self.get_long_poll()
                        continue
                    sender = self.vk_api.users.get(user_ids=sender)
                    sender = '{} {}'.format(sender[0].get('first_name'), sender[0].get('last_name'))

                    repl = repl.get('messages').get('items')[0].get('text')

                    if repl == '1':

                        self.post()
                        return
                    if repl == '2':
                        self.message_send('The next post will offered in 1 hour.')
                        time.sleep(3600)
                        self.get_long_poll()
                        break
                except IndexError:
                    print('Waiting for message...')
                    self.time_controller()
                    time.sleep(1)
                    continue
                except Exception as e:
                    print(str(e))
                    self.get_long_poll()
                    continue
