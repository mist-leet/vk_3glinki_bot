# coding=utf-8
class GSpace:

    @staticmethod
    def GetPlaces():
        places = []
        places.append(Place('Кухня'))
        places.append(Place('Раздельный сбор'))
        places.append(Place('Ванна и туалет'))
        places.append(Place('Красный ковер + крысики'))
        return places


    @staticmethod
    def GetRooms():
        rooms = [Room([
            '@id119568994 (ГЕСТ 8)'
        ], 'Восьмерка'), Room([
            '@id119568994 (Арсен)', '@id119568994 (Богдан)'
        ], 'Голубая лагуна'), Room([
            '@id119568994 (Катя)'
        ], 'Скворечник'), Room([
            '@id119568994 (Жанна)'
        ], 'Нора'), Room([
            '@id119568994 (Кристина)', '@id119568994 (Таня)'
        ], 'Белая комната'), Room([
            '@id119568994 (Аня)', '@id119568994 (Юля)'
        ], 'Аня+Юля'), Room([
            '@id119568994 (Софа)', '@id119568994 (Надя)', '@id119568994 (Паша)'
        ], 'Комната Дани'), Room([
            '@id119568994 (Илья)', '@id119568994 (Никита)', '@id119568994 (Никита)'
        ], 'Гест 4')]

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