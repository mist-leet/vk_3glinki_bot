# coding=utf-8
from vk_api.utils import get_random_id

import private
import GData
import requests
import vk_api

from vk_api.longpoll import VkLongPoll, VkEventType
from Server import BotMailer, info

class user_mailer:


    def __init__(self):
        self.mailer = []


    # True -> this element is new element
    def check(self, id):
        for m in self.mailer:
            if m.peer == id:
                return False
        return True

    def add(self, id, vk, rooms, places):
        self.mailer.append(BotMailer(vk, rooms, places, id))

session = requests.Session()
vk_session = vk_api.VkApi(token=private.__token)


longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()


duty = GData.Duty(GData.GSpace.GetRooms(), GData.GSpace.GetPlaces(), is_random=1)
d = duty.getListDuty()


mailer = BotMailer(vk, d[0], d[1])
curr_info = info(0, '')

peer = longpoll.check()[0].peer_id
print (mailer.states[mailer.state])


users = user_mailer()
users.add(vk, d[0], d[1], 0)



for event in longpoll.listen():
    if (users.check(event.peer_id)):
        users.add(vk, d[0], d[1], event.peer_id)

    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        if mailer.state == mailer.states.index('Start') and event.message == 'Показать расписание':
            mailer.sendMessage(event.peer_id, duty.getDutyMessage(), mailer.getKeyboard())
            mailer.state -= 1

            vkp = vk_api.upload.VkUpload(vk)
            data = vkp.photo_messages(duty.createIMG(), event.peer_id)

            vk.messages.send(
                peer_id=event.peer_id,
                random_id=get_random_id(),
                attachment=str('photo' + str(data[0]["owner_id"])+ '_' + str(data[0]["id"]) + '_' + str(data[0]["access_key"]))
            )

        if mailer.state == mailer.states.index('Asking'):
            if event.message == 'Нет':
                mailer.state = mailer.states.index('Start') - 1
        if mailer.state == mailer.states.index('Choice'):
            curr_info.choice = mailer.places.index(event.message)
        if mailer.state == mailer.states.index('Comment'):
            if event.message != 'Отправить без комментария':
                curr_info.comment = event.message
            else:
                curr_info.comment = 0

        mailer.send(event.peer_id, info=curr_info)

        print(mailer.states[mailer.state])