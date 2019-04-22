from Config import Config
from source.JSONWorker import JSONWorker

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import hues


class BotApi:

    def __init__(self, token):
        self.token = token
        self.vk = None
        self.users = Config.admins
        self.get_session()

    def get_session(self):
        try:
            self.vk = vk_api.VkApi(token=self.token)
        except:
            hues.error('Bad community\'s access token\\s. Or VkApi internal error.')
            exit()

    def write_msg(self, message, attachment):
        for user in self.users:
            if attachment is not None and message is not None:
                self.vk.method('messages.send', {'user_id': user, 'message': message, 'attachment': attachment,
                                                 'random_id': random.randint(0, 300000),
                                                 'keyboard': JSONWorker.read_json('default.json')})
            elif message is not None:
                self.vk.method('messages.send',
                               {'user_id': user, 'message': message, 'random_id': random.randint(0, 300000),
                                'keyboard': JSONWorker.read_json('default.json')})
            else:
                self.vk.method('messages.send',
                               {'user_id': user, 'attachment': attachment,
                                'random_id': random.randint(0, 300000),
                                'keyboard': JSONWorker.read_json('default.json')})

        return True

    def message_handler(self):
        longpoll = VkLongPoll(self.vk)

        for event in longpoll.listen():

            if event.type == VkEventType.MESSAGE_NEW:

                if event.to_me:
                    if event.user_id in Config.admins:
                        request = event.text
                        request_attach = event.attachments
                        return [request, request_attach, event.user_id]
