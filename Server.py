from vk_api.keyboard import VkKeyboard
import requests
import re

import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from GData import GSpace, Room, Place

class ChatCondition:
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

class info:
    def __init__(self, choice):
        self.choice = choice
        #self.comment = comment

class BotMailer:

    def nextState(self):
        self.state += 1
        if self.state == len(self.states):
            self.state = 0

    def previousState(self):
        self.state -= 0
        if self.state == 0:
            self.state = len(self.states)



    def getMessage(self):
        if self.state == 0:
            return '____'

    def getKeyboard(self):
        keyboard = VkKeyboard()
        if self.state == self.states.index('Mailing'):
            keyboard.add_button('Напомнить дежурным')
        elif self.state == self.states.index('Choice'):
            for i in range(len(self.places)):
                keyboard.add_button(self.places[i].name)
                if i != len(self.places) - 1:
                    keyboard.add_line()
        return keyboard.get_keyboard()

    def __init__(self, vk):
        self.vk = vk
        self.places = GSpace.GetPlaces()
        self.rooms = GSpace.GetRooms()
        self.states = [
                      'Choice',
                      'Mailing'
                      ]
        self.state = 0

    def send(self, id, info):
        if self.state == self.states.index('Choice'):
            self.sendMessage(id, self.getMessage(), self.getKeyboard())
        if self.state == self.states.index('Mailing'):
            for person in self.rooms[info.choice].members:
                self.sendMessage(get_peer_by_name(person),
                                      str('Привет, ' + person + ', ' + self.places[info.choice].name + ' ждет тебя!\n'),
                                      self.getKeyboard())
                self.sendMessage(id,
                                      str(get_name_by_name(person) + ' уведомлен\n'),
                                      self.getKeyboard())

        self.nextState()




    def sendMessage(self, id, message, keyboard):
        if keyboard != 0:
            if isinstance(id, int):
                self.vk.messages.send(
                peer_id=id,
                random_id=get_random_id(),
                message=message,
                keyboard=keyboard
                )
            elif isinstance(id, str):
                self.vk.messages.send(
                domain=id,
                random_id=get_random_id(),
                message=message,
                keyboard=keyboard
                )
        else:
            if isinstance(id, int):
                self.vk.messages.send(
                peer_id=id,
                random_id=get_random_id(),
                message=message
                )
            elif isinstance(id, str):
                self.vk.messages.send(
                domain=id,
                random_id=get_random_id(),
                message=message
                )

    def GetIndexOfPlace(self, str):
        for i in range(len(self.places)):
            if str == self.places[i].name:
                return i


class Mailer:
    def __init__(self, vk):
        self.vk = vk

    state = ChatCondition()

    places = GSpace.GetPlaces()
    rooms = GSpace.GetRooms()


    def getMessage(self):
        if self.state.condition == ChatCondition.CONDITION_ACTIVITY:
            str = 'Ребята, стоит продежурить в ближайшее время:\n'
            for s in self.rooms[q.choice]:
                str += s.name + '\n'
            return str
        if self.state.condition == ChatCondition.CONDITION_CHOICE or self.state.condition == 1:
            return 'йцу'


    def getKeyboard(self):
        type = self.state.condition
        keyboard = VkKeyboard()
        if type == 1 or type == 3:
            keyboard.add_button('Напомнить дежурным')
        elif type == 2:
            for i in range(len(self.places)):
                keyboard.add_button(self.places[i].name)
                if i != len(self.places) - 1:
                    keyboard.add_line()
        return keyboard.get_keyboard()


    def sendMessage(self, id, message, keyboard):
        if keyboard != 0:
            if isinstance(id, int):
                self.vk.messages.send(
                peer_id=id,
                random_id=get_random_id(),
                message=message,
                keyboard=keyboard
                )
            elif isinstance(id, str):
                self.vk.messages.send(
                domain=id,
                random_id=get_random_id(),
                message=message,
                keyboard=keyboard
                )
        else:
            if isinstance(id, int):
                self.vk.messages.send(
                peer_id=id,
                random_id=get_random_id(),
                message=message
                )
            elif isinstance(id, str):
                self.vk.messages.send(
                domain=id,
                random_id=get_random_id(),
                message=message
                )


    def doMailingToUser(self, id, name, place):
        self.sendMessage(id, str('Привет, ' + name + ', ' + place + ' ждет тебя!\n'), self.getKeyboard())


    def doLogToAdmin(self, id, messageTo):
        self.sendMessage(id, str(messageTo + ' уведомлен\n'), self.getKeyboard())

    def DoMailing(self, id):
        if self.state.condition == ChatCondition.CONDITION_ACTIVITY:
            for person in self.rooms[self.state.choice].members:
                self.doMailingToUser(get_peer_by_name(person), get_name_by_name(person), self.places[self.state.choice].name)
                self.doLogToAdmin(id, person)


    def GetIndexOfPlace(self, str):
        for i in range(len(self.places)):
            if str == self.places[i].name:
                return i



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


