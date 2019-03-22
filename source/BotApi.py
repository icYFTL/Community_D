import sys

sys.path.append('./source/')

from VkApiException import VkApiException
from StaticData import StaticData

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random


class BotApi:

    def __init__(self, token):
        self.token = token
        self.vk = None
        self.users = StaticData.admins
        try:
            self.vk = vk_api.VkApi(token=token)
        except:
            raise VkApiException

    def write_msg(self, message, attachment):
        for user in self.users:
            if attachment != None:
                self.vk.method('messages.send', {'user_id': user, 'message': message, 'attachment': attachment,
                                                 'random_id': random.randint(0, 300000)})
            else:
                self.vk.method('messages.send',
                               {'user_id': user, 'message': message, 'random_id': random.randint(0, 300000)})

    def message_handler(self):
        longpoll = VkLongPoll(self.vk)

        for event in longpoll.listen():

            if event.type == VkEventType.MESSAGE_NEW:

                if event.to_me:
                    request = event.text
                    print(event.info)
                    return request
