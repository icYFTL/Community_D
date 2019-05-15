from Config import Config
from source.StaticMethods import StaticMethods

import vk_api
from vk_api import exceptions
from datetime import datetime
import requests
import random
import hues


class UserApi:
    def __init__(self, token):
        self.token = token
        self.vk = None
        self.get_session()

    def get_session(self):
        try:
            self.vk = vk_api.VkApi(token=self.token)
        except:
            hues.error('Bad user\'s access token\\s. Or VkApi internal error.')
            exit()

    def posts_checker(self):
        available_posts = []
        current_date = StaticMethods.get_time().strftime('%Y-%m-%d').split('-')

        while len(available_posts) < 50:
            for i in range(len(Config.groups)):
                try:
                    posts = self.vk.method('wall.get',
                                           {'owner_id': Config.groups[random.randint(0, len(Config.groups) - 1)],
                                            'count': 10, 'offset': 0})
                    for j in range(len(posts.get('items'))):
                        if len(available_posts) >= 50:
                            break
                        post_date = datetime.utcfromtimestamp(int(posts.get('items')[j].get('date'))).strftime(
                            '%Y-%m-%d').split('-')
                        if Config.posts_fresh != None:  # important
                            for k in range(Config.posts_fresh + 1):
                                if post_date[0] == current_date[0]:
                                    if post_date[1] == current_date[1]:
                                        if int(post_date[2]) + k == int(current_date[2]):
                                            available_posts.append(posts.get('items')[j])
                                            break
                        else:
                            available_posts.append(posts.get('items')[j])
                except vk_api.exceptions.ApiError as e:
                    if '[15]' in str(e):
                        continue
        return available_posts

    def image_upload(self):

        try:
            upload_server = self.vk.method('photos.getWallUploadServer', {'group_id': int(Config.vk_community_id)})
            temp_photo = requests.post(upload_server['upload_url'],
                                       files={'photo': open('source/tmp/result.jpg', 'rb')}).json()
            save_method = \
                self.vk.method('photos.saveWallPhoto',
                               {'group_id': int(Config.vk_community_id), 'photo': temp_photo['photo'],
                                'server': temp_photo['server'],
                                'hash': temp_photo['hash']})[0]
            return 'photo{}_{}_{}'.format(save_method['owner_id'], save_method['id'], save_method['access_key'])
        except exceptions.ApiError as e:
            print(str(e))
            hues.warn('Error while image downloading. Retrying...')
            return False

    def get_user(self, user_id):
        repl = self.vk.method('users.get', {'user_id': user_id})
        repl = repl[0].get('first_name') + " " + repl[0].get('last_name')
        return repl

    def post(self, text, image):
        if text != 'False':
            self.vk.method('wall.post',
                           {'owner_id': -int(Config.vk_community_id), 'message': text, 'attachments': image})
        else:
            self.vk.method('wall.post', {'owner_id': -int(Config.vk_community_id), 'attachments': image})
