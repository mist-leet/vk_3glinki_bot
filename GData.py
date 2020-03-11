class GSpace:
    def __init__(self):
        # Гест 8
        # Голубая лагуна
        # Скворечник
        # Нора
        # Гест 4
        # Белая комната
        # Комната АЮ
        # Комната Дани
        self.rooms = []
        self.rooms.append([
            '@id119568994 (ГЕСТ 8)'
        ], 'Восьмерка')

        self.rooms.append([
            '@id119568994 (Арсен)','@id119568994 (Богдан)'
        ], 'Голубая лагуна')

        self.rooms.append([
            '@id119568994 (Катя)'
        ], 'Скворечник')

        self.rooms.append([
            '@id119568994 (Жанна)'
        ], 'Нора')

        self.rooms.append([
            '@id119568994 (Кристина)','@id119568994 (Таня)'
        ], 'Белая комната')

        self.rooms.append([
            '@id119568994 (Аня)','@id119568994 (Юля)'
        ], 'Аня+Юля')

        self.rooms.append([
            '@id119568994 (Софа)','@id119568994 (Надя)','@id119568994 (Паша)'
        ], 'Комната Дани')

        self.rooms.append([
            '@id119568994 (Илья)','@id119568994 (Никита)','@id119568994 (Никита)'
        ], 'Гест 4')

        self.places = []
        self.places.append('Кухня')
        self.places.append('Раздельный сбор')
        self.places.append('Ванна и туалет')
        self.places.append('Красный ковер + крысики')

class Room:
    def __init__(self, persons, status, name):
        self.name = name
        self.members = []
        if status == 0:
            for str in persons:
                self.members.append(str)

class Place:
    def __init__(self, place):
        self.places = []
        for str in persons:
            self.members.append(str)