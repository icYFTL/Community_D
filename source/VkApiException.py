class VkApiException(Exception):
    def __init__(self):
        print('Bad access token\\s. Or VkApi internal error.')