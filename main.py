from vk_api.keyboard import VkKeyboard
import requests
import re

import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import GData
import Server
import private

def send_message(statement, worker, id, type):
    if type == 'keyboard_only':
        vk.messages.send(
            peer_id=id,
            random_id=get_random_id(),
            message='Выберите место',
            keyboard=worker.getKeyboard(statement)
        )
    if type == 'mailing':
        vk.messages.send(
            peer_id=id,
            random_id=get_random_id(),
            message=worker.getMessage(statement),
            keyboard=worker.getKeyboard(statement)
        )


def get_id_by_name(str):
    res = re.search('@id([^\s(]*)', str)
    return int(res.group(1))


def get_name_by_name(str):
    res = re.search(r'\(([^)]*)', str)
    return res.group(1)


def get_domain_by_name(str):
    res = re.search(r'@([^\s(]*)', str)
    return res.group(1)


def get_peer_by_name(str):
    if str.find('@id') >= 0:
        return get_id_by_name(str)
    else:
        return get_domain_by_name(str)


class GlinkiCleaningInfo:
    choice = 0
    condition = 0

    CONDITION_START = 1
    CONDITION_CHOICE = 2
    CONDITION_ACTIVITY = 3

    def __init__(self):
        self.choice = -1
        self.condition = self.CONDITION_START

    def nextCondition(self):
        self.condition += 1
        if self.condition == 4:
            self.condition = 2

    def getLog(self):
        return str('ch : ' + str(self.choice) + '\n' + 'con:' + str(self.condition) + '\n')


class GlinkiCleaningt:
    rooms = [
        ['@id119568994 (Илья)', '@id119568994(Никита)', '@id119568994 (Никита)'],
        ['@id119568994 (Надя)', '@id119568994 (Софа)'],
        ['@id119568994 (Арсен)', '@id119568994 (Богдан)'],
        ['@id119568994 (ГЕСТ 8)']
    ]
    places = ['Кухня', 'Ванная', 'Красный ковер', 'Раздельный сбор']

    state = GlinkiCleaningInfo()

    def getMessage(self, q):
        if q.condition == GlinkiCleaningInfo.CONDITION_ACTIVITY:
            str = 'Ребята, стоит продежурить в ближайшее время:\n'
            for s in self.rooms[q.choice]:
                str += s + '\n'
            return str
        else:
            return q.getLog()

    def getKeyboard(self, q):
        type = q.condition
        keyboard = VkKeyboard()
        if type == 1 or type == 3:
            keyboard.add_button('Напомнить дежурным')
        elif type == 2:
            for i in range(len(self.places)):
                keyboard.add_button(self.places[i])
                if i != len(self.places) - 1:
                    keyboard.add_line()
        return keyboard.get_keyboard()

    def sendMessage(self, id, message):
        if isinstance(id, int):
            vk.messages.send(
                peer_id=id,
                random_id=get_random_id(),
                message=message
            )
        elif isinstance(id, str):
            vk.messages.send(
                domain=id,
                random_id=get_random_id(),
                message=message
            )

    def doMailingToUser(self, id, name, place):
        self.sendMessage(id, str('Привет, ' + name + ', ' + place + ' ждет тебя!\n'))

    def doLogToAdmin(self, id, messageTo):
        self.sendMessage(id, str(messageTo + ' уведомлен\n'))

    def DoMailing(self, id):
        if self.state.condition == GlinkiCleaningInfo.CONDITION_ACTIVITY:
            for person in self.rooms[self.state.choice]:
                self.doMailingToUser(get_peer_by_name(person), get_name_by_name(person), self.places[self.state.choice])
                self.doLogToAdmin(id, person)


token = __token
session = requests.Session(token=__token)
vk_session = vk_api.VkApi()

longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

cleaner = GlinkiCleaningt()
current_info = GlinkiCleaningInfo()

# send_message(current_info, cleaner, longpoll.check()[0].peer_id, 'keyboard_only')
current_info.nextCondition()

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        cleaner.state = current_info
        # GET CHOICE
        if current_info.condition == GlinkiCleaningInfo.CONDITION_ACTIVITY:
            current_info.choice = GlinkiCleaningt.places.index(event.message)
            cleaner.DoMailing(event.peer_id)
            send_message(current_info, cleaner, event.peer_id, 'keyboard_only')
            current_info.nextCondition()
            continue

        if current_info.condition == GlinkiCleaningInfo.CONDITION_CHOICE:
            send_message(current_info, cleaner, event.peer_id, 'keyboard_only')
            current_info.nextCondition()
            continue
