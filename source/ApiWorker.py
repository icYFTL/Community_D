import vk
from FileController import FileController
import random
import os
import requests
from ImageHandler import ImageHandler
from PIL import Image
from StaticData import StaticData


class ApiWorker:
    def __init__(self, token):
        self.token = token
        self.vk_api = None
        self.get_session()
        self.usedids = []

    def get_session(self):
        try:
            session = vk.Session(access_token=self.token)
            self.vk_api = vk.API(session, v='5.74')
        except:
            FileController.RemoveINI()
            return

    def get_last_posts(self):
        try:
            posts = self.vk_api.wall.get(owner_id=StaticData.groups[random.randint(0, len(StaticData.groups) - 1)],
                                         count=20)
            return posts
        except:
            print('Bad access token.\nPlease restart the script.')
            FileController.RemoveINI()
            exit()

    def parse_data(self):
        posts = self.get_last_posts()
        items = posts.get('items')

        id = random.randrange(1, len(items), 1)
        while items[id].get('id') in self.usedids:
            id = random.randrange(1, len(items), 1)

        text = items[id].get('text')
        attachment = None
        try:
            attachment = items[id].get('attachments')[0].get('photo').get('photo_807')
        except:
            try:
                attachment = items[id].get('attachments')[0].get('photo').get('photo_1280')
            except:
                pass

        return [text, attachment]

    def before_post(self):
        data = self.parse_data()

        if data[1] != '' and data[1] != None:
            try:
                os.mkdir('./source/tmp/')
            except:
                pass

            f = open('source/tmp/img.jpg', 'wb')
            f.write(requests.get(data[1]).content)
            f.close()

            img = Image.open("./source/tmp/img.jpg")
            watermark = Image.open("./source/waterx.png")

            result = ImageHandler.add_watermark(img, watermark)
            result.save('./source/tmp/result.png')

            os.remove('source/tmp/img.jpg')

            upload_server = self.vk_api.photos.getWallUploadServer(group_id=99558704)
            temp_photo = requests.post(upload_server['upload_url'],
                                       files={'photo': open('source/tmp/result.png', 'rb')}).json()
            # 'photo': b['photo'], 'server': b['server'], 'hash': b['hash']})[0]d =
            save_method = \
            self.vk_api.photos.saveWallPhoto(group_id=99558704, photo=temp_photo['photo'], server=temp_photo['server'],
                                             hash=temp_photo['hash'])[0]
            output = 'photo{}_{}'.format(save_method['owner_id'], save_method['id'])
            data = [data[0], output]
            return data

    def post(self):
        data = self.before_post()
        if data[1] is None:
            return False
        self.vk_api.wall.post(owner_id=-99558704, message=data[0], attachments=data[1])
