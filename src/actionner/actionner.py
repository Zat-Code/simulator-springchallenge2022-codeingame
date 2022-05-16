from src.actionner.entity.hero import Hero
from src.actionner.class_heroes import *
from src.actionner.entity.monster import Monster
from src.utils.vector import vector


class Actionner:

    def __init__(self, base_coordonate, player_1, player_2, entity, turn, class_heroes, get_print=None):

        self.base_coordonate = base_coordonate

        self.player_1 = player_1
        self.player_2 = player_2

        self.entity = entity

        self.get_print = get_print

        self.class_heroes = class_heroes

        self.heroes_player_1 = []
        self.heroes_player_2 = []
        self.monsters = []

        self.turn = turn

        self.SPELL_WIND_COST = 10

        self.nb_heroes = 0

        self.parseListToObject()

        self.run()

    def parseListToObject(self):

        for object in self.entity:

            if object[1] == 0:
                self.monsters.append(Monster(object[2], object[3], object[0], object[1], object[4], object[5], object[6], object[7], object[8], object[9], object[10]))

            if object[1] == 1:

                self.create_hero_with_class(object)

            if object[1] == 2:
                self.heroes_player_2.append(Hero(object[2], object[3], object[0], object[1], object[4], object[5], object[6], object[7], object[8], object[9], object[10], self.monsters, self.base_coordonate, self.player_1, self.player_2, self.turn, self.get_print))

            for hero in self.heroes_player_1:
                hero.set_heroes(self.heroes_player_2, self.heroes_player_1)

            for hero in self.heroes_player_2:
                hero.set_heroes(self.heroes_player_1, self.heroes_player_2)

    def run(self):

        for hero in self.heroes_player_1:
            hero.run()

        for hero in self.heroes_player_1:
            hero.do_action()

    def  create_hero_with_class(self, object):

        if self.turn < 100:
            class_hero_numero = self.class_heroes[self.nb_heroes]
        elif self.turn <150:
            class_hero_numero = self.class_heroes[self.nb_heroes + 3]
        else:
            class_hero_numero = self.class_heroes[self.nb_heroes + 6]

        self.nb_heroes += 1

        if class_hero_numero == 0:
            self.heroes_player_1.append(
                AttackerControlHero(object[2], object[3], object[0], object[1], object[4], object[5], object[6],
                       object[7], object[8], object[9], object[10], self.monsters,
                       self.base_coordonate, self.player_1, self.player_2, self.turn, self.get_print))

        if class_hero_numero == 1:
            self.heroes_player_1.append(
                AttackerShieldMonster(object[2], object[3], object[0], object[1], object[4], object[5], object[6],
                                    object[7], object[8], object[9], object[10], self.monsters,
                                    self.base_coordonate, self.player_1, self.player_2, self.turn, self.get_print))

        if class_hero_numero == 2:
            self.heroes_player_1.append(
                AttackerWind(object[2], object[3], object[0], object[1], object[4], object[5], object[6],
                                    object[7], object[8], object[9], object[10], self.monsters,
                                    self.base_coordonate, self.player_1, self.player_2, self.turn, self.get_print))

        if class_hero_numero == 3:
            self.heroes_player_1.append(
                DefenserControlMob(object[2], object[3], object[0], object[1], object[4], object[5], object[6],
                                    object[7], object[8], object[9], object[10], self.monsters,
                                    self.base_coordonate, self.player_1, self.player_2, self.turn, self.get_print))

        if class_hero_numero == 4:
            self.heroes_player_1.append(
                DefenserNearWind(object[2], object[3], object[0], object[1], object[4], object[5], object[6],
                                    object[7], object[8], object[9], object[10], self.monsters,
                                    self.base_coordonate, self.player_1, self.player_2, self.turn, self.get_print))

        if class_hero_numero == 5:
            self.heroes_player_1.append(
                Farmer(object[2], object[3], object[0], object[1], object[4], object[5], object[6],
                                    object[7], object[8], object[9], object[10], self.monsters,
                                    self.base_coordonate, self.player_1, self.player_2, self.turn, self.get_print))