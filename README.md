# Community_D

* `What this script does?`  
    This script steal posts from different communities and posts into yours.

* `Should I be afraid of "Nemezida"?`  
    I don't know really how works "Nemezida".
    But I can say, that we change the photo (adding watermark)
    and I haven't got any strikes yet.

* `How can I specify communities from which I'll steal the posts?`  
    You can specify them in "Config.py" in "groups".

* `I don't want to post all posts from other communities.`  
    We know that.
    We created a system, which will offer the post before posting into your group.
    Don't forget to specify your VK ID in "Config.py" in "admins".

* `Which watermark will be adding to post's image?`  
    File with watermark have to be in "png" format and called "waterx.png'.
    This file have to place in "source" folder.
    
* `Why this readme in english but script using russian?`  
    IDK XD;




#### DO NOT FORGET:
    • Specify groups in "Config.py" in "groups".
    • Specify admins in "Config.py" in "admins".
    • Speficy VK user access token in "Config.py" in "vk_user_token".  
    • Speficy VK community access token in "Config.py" in "vk_community_token".
    • Specift VK community ID in "Config.py" in "vk_community_id".  
    • Add waterx.png (watermark) into "source" directory.  
    • Do the "pip3 install -r (path_to_script)/requirements.txt"

#### Tokens's rights:  
##### 1) User: 
    wall,offline,groups,photos
##### 2) Community:
    messages,wall,photos

Get [token](https://oauth.vk.com/authorize?client_id=6949573&scope=wall,offline,groups,photos&redirect_uri=https://oauth.vk.com/blank.html&display=page&response_type=token&revoke=1 "Get user's access token VK")

Token is string which length is 85 symbols.  
It begins from `"access_token="` ***(without '=')*** to `&`   


That's all what I have to say.  
Hope that this script will help you with your communities.

Best regards `icYFTL`


