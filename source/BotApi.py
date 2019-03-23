from VkApiException import VkApiException
from Config import StaticData

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random


class BotApi:

    def __init__(self, token):
        self.token = token
        self.vk = None
        self.users = StaticData.admins
        self.get_session()

    def get_session(self):
        try:
            self.vk = vk_api.VkApi(token=self.token)
        except:
            raise VkApiException

    def write_msg(self, message, attachment):
        for user in self.users:
            if attachment is not None and message is not None:
                self.vk.method('messages.send', {'user_id': user, 'message': message, 'attachment': attachment,
                                                 'random_id': random.randint(0, 300000)})
            elif message is not None:
                self.vk.method('messages.send',
                               {'user_id': user, 'message': message, 'random_id': random.randint(0, 300000)})
            else:
                self.vk.method('messages.send',
                               {'user_id': user, 'attachment': attachment, 'random_id': random.randint(0, 300000)})

        return True

    def message_handler(self):
        longpoll = VkLongPoll(self.vk)

        for event in longpoll.listen():

            if event.type == VkEventType.MESSAGE_NEW:

                if event.to_me:
                    if event.user_id in StaticData.admins:
                        request = event.text
                        return [request, event.user_id]
