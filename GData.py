# coding=utf-8
import random
import itertools
from PIL import Image, ImageFont, ImageDraw


class GSpace:

    @staticmethod
    def GetPlaces():
        places = []
        places.append('Кухня')
        places.append('Раздельный сбор')
        places.append('Ванная и туалет')
        places.append('Красный ковер + крысики')
        return places


    @staticmethod
    def GetRooms():

        rooms = [
        Room([
            '@id119568994 (Илья)', '@id221460353 (Никита)', '@sarsit(Никита)', '@id152207052 (Андрей)'
        ], 'Гест 4'),
        Room([
            '@1anastasia (Робототехника)', '@piiligriim (Сергей)'
        ], 'Восьмерка'),
        Room([
            '@emshv_arsn (Арсен)', '@oslivizan (Богдан)'
        ], 'Голубая лагуна'),
        Room([
            '@id82573049 (Катя)'
        ], 'Скворечник'),
        Room([
            '@id529306038 (Жанна)'
        ], 'Нора'),
        Room([
            '@silvermarten (Таня)', '@askarbina (Катя)'
        ], 'Белая комната'),
        Room([
            '@n_mori_an (Аня)', '@id16144866 (Юля)'
        ], 'Аня+Юля'),
        Room([
            '@id133687981 (Софа)', '@dinaroy (Надя)', '@auroborous (Паша)'
        ], 'Софа+Надя+Паша'),
        Room([
            '@tdamrina (Таня)'
        ], 'Красная комната'),
        Room([
            '@solorman (Руслан)', '@nasiba1801 (Настя В)'
        ], 'Руслан Настя'),
        Room([
            '@id109997707 (Леша)'
        ], 'Цветник')
        ]
        return rooms


class Room:
    def __init__(self, persons, name):
        self.name = name
        self.members = []
        for str in persons:
            self.members.append(str)


class Place:
    def __init__(self, name):
        self.name = name


class duty_el:
    def __init__(self, person, place):
        self.person = person
        self.place = place




class Duty:

    def __init__(self, rooms, places, is_random = 0):
        self.duty = []
        if is_random == 0:
            rooms_copy = rooms
            random.shuffle(rooms_copy)
            for i in range(len(places)):
                self.duty.append(duty_el(rooms_copy[i], places[i]))
        elif is_random == 1:
            self.duty.append(duty_el((rooms[1]), places[0])) #  Kitchen
            self.duty.append(duty_el((rooms[7]), places[1])) #  Trash
            self.duty.append(duty_el((rooms[5]), places[2])) #  Bath
            self.duty.append(duty_el((rooms[2]), places[3])) #  Carpet


    def getListDuty(self):
        rooms = []
        places = []

        for el in (self.duty):
            rooms.append(el.person)
            places.append(el.place)
        return [rooms, places]

    def getDutyMessage(self):
        str = ''
        for i in self.duty:
            str += i.place + ' : ' + i.person.name + '\n'
        return str

    def createIMG(self):
        img = Image.new('RGB', (1200, 270), color = (255, 255, 255))
        d = ImageDraw.Draw(img)
        font = ImageFont.truetype("ex/working/x.otf", 60)
        str = ''
        for s in self.duty:
            str += s.place + ' : ' + s.person.name + '\n'
        d.multiline_text((20,20), str, fill=(0,0,0), font=font)
        #for i in range(len(self.duty)):
        #    d.text((10 , 10 + i * 10), str(self.duty[i].place + " : " + self.duty[i].person.name), fill=(255, 255, 0),
        #           font=font)

        img.save('duty.png')
        return  'duty.png'

