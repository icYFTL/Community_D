import sys

sys.path.append('./source/')

from VkApiException import VkApiException
from StaticData import StaticData
from StaticMethods import StaticMethods

import vk_api
import time
from datetime import datetime
import requests


class UserApi:
    def __init__(self, token):
        self.token = token
        self.vk = None
        self.get_session()

    def get_session(self):
        try:
            self.vk = vk_api.VkApi(token=self.token)
        except:
            raise VkApiException

    def posts_checker(self):
        available_posts = []
        current_date = StaticMethods.get_time().strftime('%Y-%m-%d').split('-')

        for i in StaticData.groups:
            posts = self.vk.method('wall.get', {'owner_id': int(i), 'count': 20, 'offset': 0})

            for j in range(len(posts.get('items'))):
                post_date = datetime.utcfromtimestamp(int(posts.get('items')[j].get('date'))).strftime(
                    '%Y-%m-%d').split('-')
                if post_date == current_date:
                    available_posts.append(posts.get('items')[j])
            time.sleep(0.4)
        if len(available_posts) < 1:
            return False
        return available_posts

    def image_upload(self):

        upload_server = self.vk.method('photos.getWallUploadServer', {'group_id': 99558704})
        temp_photo = requests.post(upload_server['upload_url'],
                                   files={'photo': open('source/tmp/result.png', 'rb')}).json()
        save_method = \
            self.vk.method('photos.saveWallPhoto', {'group_id': 99558704, 'photo': temp_photo['photo'],
                                                    'server': temp_photo['server'],
                                                    'hash': temp_photo['hash']})[0]
        return 'photo{}_{}_{}'.format(save_method['owner_id'], save_method['id'], save_method['access_key'])

    def get_user(self, id):
        repl = self.vk.method('users.get', {'user_id': id})
        repl = repl[0].get('first_name') + " " + repl[0].get('last_name')
        return repl

    def post(self, text, image):
        if text is not None:
            self.vk.method('wall.post', {'owner_id': -99558704, 'message': text, 'attachments': image})
        elif text is None:
            self.vk.method('wall.post', {'owner_id': -99558704, 'attachments': image})
