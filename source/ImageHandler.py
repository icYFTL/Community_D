from PIL import Image
from PIL import ImageEnhance
import random


class ImageHandler(object):
    """
    image - картинка, на которую накладываете изображение
    watermark - картинка, которую накладываете
    opacity - прозрачность
    wm_interval - интервал между изображениями watermark
    """

    def add_watermark(image, watermark, opacity=1, wm_interval=0):

        assert opacity >= 0 and opacity <= 1
        if opacity < 1:
            if watermark.mode != 'RGBA':
                watermark = watermark.convert('RGBA')
            else:
                watermark = watermark.copy()
            alpha = watermark.split()[3]
            alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
            watermark.putalpha(alpha)
        layer = Image.new('RGBA', (1280, 640), (0, 0, 0, 0))
        a = random.randint(-20, 0)
        b = random.randint(-20, 0)
        layer.paste(watermark, (a, b))

        return Image.composite(layer, image, layer)
