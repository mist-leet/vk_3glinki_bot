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
        places.append('Ванна и туалет')
        places.append('Красный ковер + крысики')
        return places


    @staticmethod
    def GetRooms():
        rooms = [
        Room([
            '@id119568994 (Илья)', '@id119568994 (Никита)', '@id119568994 (Никита)'
        ], 'Гест 4'),
        Room([
            '@ebeniesexom (ГЕСТ 8)'
        ], 'Восьмерка'),
        Room([
            '@id119568994 (Арсен)', '@id119568994 (Богдан)'
        ], 'Голубая лагуна'),
        Room([
            '@id119568994 (Катя)'
        ], 'Скворечник'),
        Room([
            '@id119568994 (Жанна)'
        ], 'Нора'),
        Room([
            '@id119568994 (Кристина)', '@id119568994 (Таня)'
        ], 'Белая комната'),
        Room([
            '@id119568994 (Аня)', '@id119568994 (Юля)'
        ], 'Аня+Юля'),
        Room([
            '@id119568994 (Софа)', '@id119568994 (Надя)', '@id119568994 (Паша)'
        ], 'Комната Дани')]

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
            for i in range(len(places)):
                self.duty.append(duty_el(rooms[i], places[i]))


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
        img = Image.new('RGB', (1100, 250), color = (255, 255, 255))
        d = ImageDraw.Draw(img)
        font = ImageFont.truetype("ex/working/x.otf", 60)
        str = ''
        for s in self.duty:
            str += s.place + ' : ' + s.person.name + '\n'
        d.multiline_text((10,10), str, fill=(0,0,0), font=font)
        #for i in range(len(self.duty)):
        #    d.text((10 , 10 + i * 10), str(self.duty[i].place + " : " + self.duty[i].person.name), fill=(255, 255, 0),
        #           font=font)

        img.save('duty.png')
        return  'duty.png'

