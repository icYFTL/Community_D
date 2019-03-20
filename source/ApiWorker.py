import vk
from FileController import FileController
import random
import os
import requests
from ImageHandler import ImageHandler
from PIL import Image
from StaticData import StaticData
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
        self.available_groups = []

    def get_long_poll(self):
        self.community_long_poll = self.vk_api_c.messages.getLongPollServer(need_pts=1)

    def get_session(self):
        try:
            session = vk.Session(access_token=self.token)
            self.vk_api = vk.API(session, v='5.74')

            commsession = vk.Session(access_token=self.commtoken)
            self.vk_api_c = vk.API(commsession, v='5.92')
        except:
            FileController.RemoveINI()
            return

    def groups_checker(self):
        current_date = datetime.now().strftime('%Y-%m-%d').split('-')
        for i in StaticData.groups:

            posts = self.vk_api.wall.get(owner_id=int(i),
                                         count=20, offset=0)
            for j in range(len(posts.get('items'))):
                post_date = datetime.utcfromtimestamp(int(posts.get('items')[j].get('date'))).strftime(
                    '%Y-%m-%d').split('-')
                if post_date == current_date:
                    self.available_groups.append(posts.get('items')[j])
            time.sleep(1)
        if self.available_groups is []:
            return False

    def parse_data(self):
        while True:
            if self.groups_checker() is False:
                print('No available posts at groups. I\'ll try later.')
                time.sleep(3600)
                continue
            else:
                break
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
                    try:
                        attachment = j.get('photo').get('photo_2560')
                    except:
                        try:
                            attachment = j.get('photo').get('photo_1280')
                        except:
                            try:
                                attachment = j.get('photo').get('photo_807')
                            except:
                                continue
            return [text, attachment]

    def before_post(self):
        data = self.parse_data()
        while data is None:
            data = self.parse_data()
            time.sleep(1)

        if data[1] != '':
            try:
                os.mkdir('./source/tmp/')
            except:
                pass

            f = open('source/tmp/img.jpg', 'wb')
            while True:
                try:
                    f.write(requests.get(data[1]).content)
                    break
                except requests.exceptions.MissingSchema:
                    time.sleep(1)
                    continue
            f.close()

            ## WATERMARK LANDING ##

            img = Image.open("./source/tmp/img.jpg")
            watermark = Image.open("./source/waterx.png")

            result = ImageHandler.add_watermark(img, watermark)
            result.save('./source/tmp/result.png')

            os.remove('source/tmp/img.jpg')

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

            ## ACCEPTABLE MESSAGE SENDING

            self.vk_api_c.messages.send(user_id=239125937, message=data[0],
                                        attachment="photo" + str(save_method['owner_id']) + "_" + str(
                                            save_method['id']) + "_" +
                                                   str(save_method['access_key']),
                                        random_id=random.randint(0, 10000))
            self.vk_api_c.messages.send(user_id=239125937,
                                        message="Accept post?\nYou can:\n1 - Accept\n2 - Show next",
                                        random_id=random.randint(0, 10000))

            self.get_long_poll()

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

                    self.get_long_poll()

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
                    time.sleep(1)
                    continue
                except Exception as e:
                    print(str(e))
                    self.get_long_poll()
                    continue

            return data

    def post(self):
        data = self.before_post()
        if data is False:
            self.post()
            return
        if data[1] is None:
            return False
        self.vk_api.wall.post(owner_id=-99558704, message=data[0], attachments=data[1])
