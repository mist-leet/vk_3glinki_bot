# coding=utf-8
from vk_api.keyboard import VkKeyboard
import requests
import re
from datetime import datetime, date, time

import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from GData import GSpace, Room, Place


class info:
    def __init__(self, choice, comment=None, date=None):
        self.choice = choice
        self.comment = comment
        self.date = date

    def getComment(self):
        if self.comment == 0 or self.comment == 'Отправить без комментария':
            return ''
        else:
            return 'Комментарий: ' + self.comment


class Log:
    def __init__(self):
        self.places = GSpace.GetPlaces()
        self.LOG = []
        for i in range(len(self.places)):
            self.LOG.append([self.places[i], 0])

    def DoLog(self, str):
        self.LOG[self.places.index(str)][1] = datetime.now()

    def CheckLogMessage(self, str):
        delta = self.LOG[self.places.index[str]][1].timedelta(datetime.now())
        return "Последний раз сообщения по месту '" + str + "' приходили " + delta + '. Все равно отправить?'

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
        return '____'

    def getKeyboard(self):
        keyboard = VkKeyboard()
        if self.state == self.states.index('Start'):
            keyboard.add_button('Напомнить дежурным')
        elif self.state == self.states.index('Choice'):
            for i in range(len(self.places)):
                keyboard.add_button(self.places[i])
                if i != len(self.places) - 1:
                    keyboard.add_line()
        elif self.state == self.states.index('Comment'):
            keyboard.add_button('Отправить без комментария')
            # return VkKeyboard().get_empty_keyboard()
        else:
            return VkKeyboard().get_empty_keyboard()
        return keyboard.get_keyboard()

    def __init__(self, vk):
        self.vk = vk
        self.places = GSpace.GetPlaces()
        self.rooms = GSpace.GetRooms()
        self.states = [
            'Start',
            'Choice',
            'Comment',
            'Mailing'
        ]
        self.state = 0
        self.log = Log()

    def send(self, id, info):
        self.nextState()
        if self.state == self.states.index('Start'):
            self.sendMessage(id, self.getMessage(), self.getKeyboard())
        if self.state == self.states.index('Choice'):
            self.sendMessage(id, self.getMessage(), self.getKeyboard())
        if self.state == self.states.index('Mailing'):
            for person in self.rooms[info.choice].members:
                self.sendMessage(get_peer_by_name(person),
                                 str('Привет, ' + person + ', ' + self.places[
                                     info.choice] + ' ждет тебя!\n' + info.getComment()),
                                 self.getKeyboard())

                self.sendMessage(id,
                                 str(get_name_by_name(person) + ' уведомлен\n'),
                                 self.getKeyboard())
                self.log.DoLog(self.places[info.choice])
                #!
                for a in self.log.LOG:
                    print(a)
                #!
                self.send(id, info)
        if self.state == self.states.index('Comment'):
            self.sendMessage(id, "Введите комментарий или нажмите 'Отправить без комментария'", self.getKeyboard())

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
            if str == self.places[i]:
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
