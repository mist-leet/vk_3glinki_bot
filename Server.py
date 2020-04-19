# coding=utf-8
from vk_api.keyboard import VkKeyboard
import re
from datetime import datetime
from vk_api.utils import get_random_id
import cv2

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
            self.LOG.append([self.places[i], datetime.now()])

    def DoLog(self, str):
        self.LOG[self.places.index(str)][1] = datetime.now()

    def CheckLogMessage(self, str):
        delta = self.LOG[self.places.index[str]][1].timedelta(datetime.now())
        return "Последний раз сообщения по месту '" + str + "' приходили " + delta + '. Все равно отправить?'

class Camera:

    @staticmethod
    def getPic():
        webcam = cv2.VideoCapture(0)
        try:
            check, frame = webcam.read()
            print(check)  # prints true as long as the webcam is running
            cv2.imshow("Capturing", frame)
            cv2.imwrite(filename='img.jpg', img=frame)
            webcam.release()
            print("Processing image...")

        except(KeyboardInterrupt):
            print("Turning off camera.")
            webcam.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
        return 'img.jpg'

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
            keyboard.add_line()
            keyboard.add_button('Показать расписание')
        elif self.state == self.states.index('Choice'):
            for i in range(len(self.places)):
                keyboard.add_button(self.places[i])
                if i != len(self.places) - 1:
                    keyboard.add_line()
        elif self.state == self.states.index('Comment'):
            keyboard.add_button('Отправить без комментария')
        elif self.state == self.states.index('Asking'):
            keyboard.add_button('Да')
            keyboard.add_button('Нет')
        else:
            return VkKeyboard().get_empty_keyboard()
        return keyboard.get_keyboard()

    def __init__(self, vk, rooms, places, peer):
        self.peer = peer
        self.vk = vk
        self.places = places
        self.rooms = rooms
        self.states = [
            'Start',
            'Choice',
            'Comment',
            'Asking',
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
                is_ok = self.sendMessage(get_peer_by_name(person),
                                 str('Привет, ' + person + ', ' + self.places[
                                     info.choice] + ' ждет тебя!\n' + info.getComment()),
                                 self.getKeyboard())
                if is_ok:
                    self.sendMessage(id,
                                 str(get_name_by_name(person) + ' уведомлен\n'),
                                 self.getKeyboard())
            self.log.DoLog(self.places[info.choice])
            self.send(id, info)

        if self.state == self.states.index('Comment'):
            self.sendMessage(id, "Введите комментарий или нажмите 'Отправить без комментария'", self.getKeyboard())
        if self.state == self.states.index('Asking'):
            self.sendMessage(id, str('Сообщение о ' + self.places[info.choice] + ' было отправлено ' +
                                     (self.log.LOG[info.choice][1]).strftime('%d ') + 'числа в ' + (self.log.LOG[info.choice][1]).strftime('%H:%M ') +
                                     ', все равно отправить?'), self.getKeyboard())

    def sendMessage(self, id, message, keyboard):
        try:
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

            return True
        except:
            print('user ' + str(id) + ' is unregistred')
            return False

    def getNameById(self, id):
        for room in self.rooms:
            for person in room.members:
                if person.find(str(id)) >= 0:
                    return get_name_by_name(person)


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
