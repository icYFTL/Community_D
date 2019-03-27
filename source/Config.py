class StaticData:
    groups = []  # Communities IDs like [-123456789, -987654321 ... ] *Minus is important
    admins = []  # Users IDs like [123456789 , 987654321 ... ]
    vk_user_token = ""  # Change "" on your VK user access token like "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    vk_community_token = ""  # Change "" on your VK community access token like "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    vk_community_id = ""  # Change "" on your VK community ID like "123456789" *without mines*
    workout_time = [11,
                    23]  # Change this values on your own. For example: [11, 23] - 11 PM scripts starts, 23 AM - scripts going to sleep up to 11. Or you can off this time-checking by "workout_time = None"
    posts_fresh = None  # Change this value on your own. For example: 1 means that post with date 28.03.2019 comparing with today's date (29.03.2019) will be accepted. Or you can off this time-checking by "posts_fresh = None"
