from src.actionner.entity.hero import Hero
from src.utils.vector import vector
import random


class AttackerControlHero(Hero):

    def __init__(self,  x, y, id, type_character, shield_life, is_controlled, health, vx, vy, near_base, threat_for, monsters, base_coordonate, player_1, player_2, turn, get_print=None):
        super().__init__(x, y, id, type_character, shield_life, is_controlled, health, vx, vy, near_base, threat_for, monsters, base_coordonate, player_1, player_2, turn, get_print=get_print)


        if self.base_coordonate.x == 0:
            self.base_coordonate_ennemy = vector(17630, 9000)
        else:
            self.base_coordonate_ennemy = vector(0, 0)

    def run(self):


        self.do_random_move()

        if not (self.check_point_on_circle(self.position, self.base_coordonate_ennemy, 6000)) or self.check_point_on_circle(
                self.position, self.base_coordonate_ennemy, 4000):
            self.move(self.base_coordonate_ennemy.x, self.base_coordonate_ennemy.y)

        self.check_if_control_hero_is_possible()
        self.check_if_shield_is_possible()
        self.check_if_control_monster_is_possible()
        self.check_if_wind_is_possible()
        self.check_for_perfect_wind()


    def check_if_control_monster_is_possible(self):

        if self.player_1[1] >= self.SPELL_COST:

            entities = []

            for monster in self.monsters:

                if monster.shield_life == 0 and monster.threat_for != 2 and monster.near_base == 0:
                    ret = self.check_if_monster_is_in_control_and_shield_range(monster)

                    if ret == 1:
                        entities.append(monster)

            for entity in entities:
                if self.player_1[1] >= self.SPELL_COST:
                    self.control(entity.id, vector(self.base_coordonate_ennemy.x, self.base_coordonate_ennemy.y))

    def check_if_control_hero_is_possible(self):

        if self.player_1[1] >= 100:

            entities = []

            for hero in self.heroes_ennemy:

                if hero.shield_life == 0 and hero.process_distance_hero2base(self.base_coordonate_ennemy) <= 9000:
                    ret = self.check_if_monster_is_in_control_and_shield_range(hero)

                    if ret == 1:
                        entities.append(hero)

            for entity in entities:
                if self.player_1[1] >= self.SPELL_COST:
                    self.control(entity.id, vector(self.base_coordonate.x, self.base_coordonate.y))

    def check_if_shield_is_possible(self):

        if self.player_1[1] >= self.SPELL_COST:

            entities = []

            for monster in self.monsters:
                monster.process_distance_monster2base(self.base_coordonate_ennemy)
                if monster.shield_life == 0 and monster.distance_monster2base <= 5300 and monster.threat_for == 2:
                    ret = self.check_if_monster_is_in_control_and_shield_range(monster)

                    if ret == 1:
                        entities.append(monster)

            for entity in entities:
                if self.player_1[1] >= self.SPELL_COST:
                    self.shield(entity.id)

    def check_if_wind_is_possible(self):

        if self.player_1[1] >= self.SPELL_COST:

            entities = []

            nb_monster_in_wind = 0
            monster_in_wind = []
            for monster in self.monsters:
                monster.process_distance_monster2base(self.base_coordonate_ennemy)
                if monster.shield_life == 0 and monster.distance_monster2base <= 9000:

                    ret = self.check_if_monster_is_in_wind_range(monster)
                    nb_monster_in_wind += ret

                    if ret == 1:
                        monster_in_wind.append(monster)

                    entities.append([nb_monster_in_wind, monster_in_wind])

            for entity in entities:
                if self.player_1[1] >= self.SPELL_COST:
                    if entity[0] >= 4:
                        wind_trajectory = self.position + self.base_coordonate_ennemy
                        self.wind(wind_trajectory)

                        self.player_1 = (self.player_1[0], self.player_1[1] - self.SPELL_COST)

    def check_for_perfect_wind(self):

        for monster in self.monsters:
            monster.process_distance_monster2monsters(self.monsters)
            monster.process_distance_monster2base(self.base_coordonate_ennemy)
            if monster.number_monster_near > 3 and monster.distance_monster2base <= 8000:
                self.move(monster.position.x, monster.position.y)


    def do_random_move(self):

        move_is_ok = False
        compteur = 0
        while not move_is_ok:

            x = random.randint(-100, 100)
            y = random.randint(-100, 100)

            if x != 0 and y!= 0:

                futur_position = self.position + (vector(x, y).get_unit_vector() * 400)
                futur_position = futur_position.int()

                position_check = 0 < futur_position.x < 17630 and 0 < futur_position.y < 9000
                circle_check = self.check_point_on_circle(futur_position, self.base_coordonate_ennemy, 8000) and not(self.check_point_on_circle(futur_position, self.base_coordonate_ennemy, 5000))

                move_is_ok = position_check and circle_check
                compteur += 1
                if compteur > 100:
                    break
        self.move(futur_position.x, futur_position.y)