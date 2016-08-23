# -*- coding: utf-8 -*-

"""
@author: Kirill Python
@contact: https://vk.com/python273
"""

import vk_api


def main():
#login, password = 'python@vk.com', 'mypassword'
#    vk_session = vk_api.VkApi(login, password)

#    try:
#        vk_session.authorization()
#    except vk_api.AuthorizationError as error_msg:
#        print(error_msg)
#        return

#    vk = vk_session.get_api()

    response = vk.wall.get(count=1,owner_id=1)  
    if response['items']:
        print(response['items'][0])

if __name__ == '__main__':
    main()
