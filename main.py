import GData
import Server
import private

import re
import requests
import vk_api

from vk_api.longpoll import VkLongPoll, VkEventType
from GData import GSpace, Room, Place
from Server import BotMailer, info

session = requests.Session()
vk_session = vk_api.VkApi(token=private.__token)

longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

mailer = BotMailer(vk)
curr_info = info(0)
mailer.send(longpoll.check()[0].peer_id, info=curr_info)

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        if mailer.state == mailer.states.index('Mailing'):
            curr_info.choice = mailer.GetIndexOfPlace(event.message)
        mailer.send(event.peer_id, info=curr_info)

