from VkApiException import VkApiException
from Config import StaticData
from StaticMethods import StaticMethods

import vk_api
from vk_api import exceptions
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
            try:
                posts = self.vk.method('wall.get', {'owner_id': int(i), 'count': 20, 'offset': 0})

                for j in range(len(posts.get('items'))):
                    post_date = datetime.utcfromtimestamp(int(posts.get('items')[j].get('date'))).strftime(
                        '%Y-%m-%d').split('-')
                    if post_date == current_date:
                        available_posts.append(posts.get('items')[j])
                time.sleep(0.4)
            except vk_api.exceptions.ApiError as e:
                if '[15]' in str(e):
                    continue
        if len(available_posts) < 1:
            return False
        return available_posts

    def image_upload(self):

        try:
            upload_server = self.vk.method('photos.getWallUploadServer', {'group_id': int(StaticData.vk_community_id)})
            temp_photo = requests.post(upload_server['upload_url'],
                                       files={'photo': open('source/tmp/result.png', 'rb')}).json()
            save_method = \
                self.vk.method('photos.saveWallPhoto',
                               {'group_id': int(StaticData.vk_community_id), 'photo': temp_photo['photo'],
                                'server': temp_photo['server'],
                                'hash': temp_photo['hash']})[0]
            return 'photo{}_{}_{}'.format(save_method['owner_id'], save_method['id'], save_method['access_key'])
        except exceptions.ApiError:
            print('Error while image downloading. Retrying...')
            return False

    def get_user(self, user_id):
        repl = self.vk.method('users.get', {'user_id': user_id})
        repl = repl[0].get('first_name') + " " + repl[0].get('last_name')
        return repl

    def post(self, text, image):
        if text is not None:
            self.vk.method('wall.post',
                           {'owner_id': -int(StaticData.vk_community_id), 'message': text, 'attachments': image})
        elif text is None:
            self.vk.method('wall.post', {'owner_id': -int(StaticData.vk_community_id), 'attachments': image})
