from PIL import Image
import random


class ImageHandler:

    @staticmethod
    def watermark_with_transparency(image):
        base_image = Image.open(image)
        watermark = ImageHandler.watermark_resizer(base_image, Image.open('source/waterx.png'))
        width, height = base_image.size
        widthw, heightw = watermark.size

        transparent = Image.new('RGB', (width, height), (0, 0, 0, 0))
        transparent.paste(base_image, (0, 0))
        position = (random.randint(0, width - widthw), random.randint(0, height - heightw))
        transparent.paste(watermark, position, mask=watermark)
        transparent.save('source/tmp/result.jpg')

    @staticmethod
    def watermark_resizer(image, watermark):
        if image.size[0] < 605 or image.size[1] < 605:
            return watermark.resize((200, 200))
        elif image.size[0] < 807 or image.size[1] < 807:
            return watermark.resize((250, 250))
        elif image.size[0] < 1080 or image.size[1] < 1024:
            return watermark.resize((300, 300))
        elif image.size[0] < 2560 or image.size[1] < 2048:
            return watermark.resize((600, 600))
        return watermark.resize((300, 300))
