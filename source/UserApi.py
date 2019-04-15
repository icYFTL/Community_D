from Config import Config
from source.StaticMethods import StaticMethods

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
            print('Bad user\'s access token\\s. Or VkApi internal error.')
            exit()

    def posts_checker(self):
        available_posts = []
        current_date = StaticMethods.get_time().strftime('%Y-%m-%d').split('-')

        for i in Config.groups:
            try:
                posts = self.vk.method('wall.get', {'owner_id': int(i), 'count': 50, 'offset': 0})

                for j in range(len(posts.get('items'))):
                    post_date = datetime.utcfromtimestamp(int(posts.get('items')[j].get('date'))).strftime(
                        '%Y-%m-%d').split('-')
                    if Config.posts_fresh:
                        for k in range(Config.posts_fresh):
                            if post_date[0] == current_date[0]:
                                if post_date[1] == current_date[1]:
                                    if int(post_date[2]) + k == int(current_date[2]):
                                        available_posts.append(posts.get('items')[j])
                                        break
                    else:
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
            upload_server = self.vk.method('photos.getWallUploadServer', {'group_id': int(Config.vk_community_id)})
            temp_photo = requests.post(upload_server['upload_url'],
                                       files={'photo': open('source/tmp/result.png', 'rb')}).json()
            save_method = \
                self.vk.method('photos.saveWallPhoto',
                               {'group_id': int(Config.vk_community_id), 'photo': temp_photo['photo'],
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
                           {'owner_id': -int(Config.vk_community_id), 'message': text, 'attachments': image})
        elif text is None:
            self.vk.method('wall.post', {'owner_id': -int(Config.vk_community_id), 'attachments': image})
