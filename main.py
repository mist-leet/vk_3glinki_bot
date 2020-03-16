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
        self.info = []
    # True -> this element is new element
    def check(self, id):
        for m in self.mailer:
            if m.peer == id:
                return False
        return True

    def add(self,vk, rooms, places, id, info):
        self.mailer.append(BotMailer(vk, rooms, places, id))
        self.info.append(info)

    def get(self, id):
        for m in self.mailer:
            if m.peer == id:
                return m

    def getI(self, id):
        return self.info[self.mailer.index(self.get(id))]

def log(mailer):
    print('user: ' + str(mailer.peer) + ' state: ' + str(mailer.states[mailer.state]))

session = requests.Session()
vk_session = vk_api.VkApi(token=private.__token)


longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()


duty = GData.Duty(GData.GSpace.GetRooms(), GData.GSpace.GetPlaces(), is_random=1)
d = duty.getListDuty()


#curr_info = info(0, '')

users = user_mailer()
users.add(vk, d[0], d[1], 0, info(0, ''))


for event in longpoll.listen():
    if (users.check(event.peer_id)):
        users.add(vk, d[0], d[1], event.peer_id, info(0, ''))

    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        peer = event.peer_id
        if users.get(peer).state == users.get(peer).states.index('Start') and event.message == 'Показать расписание':
            users.get(peer).sendMessage(event.peer_id, duty.getDutyMessage(), users.get(peer).getKeyboard())
            users.get(peer).state -= 1

            vkp = vk_api.upload.VkUpload(vk)
            data = vkp.photo_messages(duty.createIMG(), event.peer_id)

            vk.messages.send(
                peer_id=event.peer_id,
                random_id=get_random_id(),
                attachment=str('photo' + str(data[0]["owner_id"])+ '_' + str(data[0]["id"]) + '_' + str(data[0]["access_key"]))
            )

        if users.get(peer).state == users.get(peer).states.index('Asking'):
            if event.message == 'Нет':
                users.get(peer).state = users.get(peer).states.index('Start') - 1
        if users.get(peer).state == users.get(peer).states.index('Choice'):
            users.getI(peer).choice = users.get(peer).places.index(event.message)
        if users.get(peer).state == users.get(peer).states.index('Comment'):
            if event.message != 'Отправить без комментария':
                users.getI(peer).comment = event.message
            else:
                users.getI(peer).comment = 0

        users.get(peer).send(event.peer_id, info=users.getI(peer))

        log(users.get(peer))