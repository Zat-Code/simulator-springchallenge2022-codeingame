from src.actionner.entity.hero import Hero
from src.utils.vector import vector
import random


class DefenserNearWind(Hero):

    def __init__(self,  x, y, id, type_character, shield_life, is_controlled, health, vx, vy, near_base, threat_for, monsters, base_coordonate, player_1, player_2, turn, get_print=None):
        super().__init__(x, y, id, type_character, shield_life, is_controlled, health, vx, vy, near_base, threat_for, monsters, base_coordonate, player_1, player_2, turn, get_print=get_print)


    def run(self):

        self.check_near_monster()
        self.check_if_wind_is_possible()
        self.check_if_shield_is_possible()

        pos_start = {0: (4077, 2851),
                     1: (4923, 1119),
                     2: (1654, 4612),
                     3: (14011, 5575),
                     4: (12717, 7638),
                     5: (15373, 4573)}

        if self.turn < 3:
            if self.base_coordonate.x == 0:
                self.move(pos_start[self.id][0], pos_start[self.id][1])
            else:
                self.move(pos_start[self.id][0], pos_start[self.id][1])

    def check_near_monster(self):

        for monster in self.monsters:
            monster.process_distance_monster2base(self.base_coordonate)

        monsters_sort = self.monsters.copy()

        monsters_sort.sort(key=lambda monster: monster.distance_monster2base)

        monster_find = False
        for monster in monsters_sort:
            if monster.is_cibled == 0 and (monster.threat_for == 1 or monster.near_base == 1) and monster.distance_monster2base < 8000:
                    self.move(monster.position.x, monster.position.y)
                    monster.is_cibled = 1
                    monster_find = True
                    break
        if not monster_find:
            if not monster_find:
                if len(monsters_sort) == 0:
                    self.wait()
                else:
                    if 0 < monsters_sort[0].position.x < 17630 and 0 < monsters_sort[0].position.y < 9000:
                        self.move(monsters_sort[0].position.x, monsters_sort[0].position.y)
                    else:
                        self.wait()

    def check_if_wind_is_possible(self):

        if self.player_1[1] >= self.SPELL_COST:

            entities = []

            nb_monster_in_wind = 0
            monster_in_wind = []
            for monster in self.monsters:
                monster.process_distance_monster2base(self.base_coordonate)
                if monster.shield_life == 0 and monster.distance_monster2base < 1500 and monster.health > 6:

                    ret = self.check_if_monster_is_in_wind_range(monster)
                    nb_monster_in_wind += ret

                    if ret == 1:
                        monster_in_wind.append(monster)

                    entities.append([nb_monster_in_wind, monster_in_wind])

            for entity in entities:
                if self.player_1[1] >= self.SPELL_COST:
                    if entity[0] >= 1:
                        sum_trajectory_monster = vector(0, 0)
                        for monster in entity[1]:
                            sum_trajectory_monster += monster.trajectory

                        mean_trajectory = (sum_trajectory_monster/len(entity[1])).int()
                        wind_trajectory = self.position + mean_trajectory.inv()
                        self.wind(wind_trajectory)
                        # self.control(wind[1][0].id, vector(0, 0))

                        self.player_1 = (self.player_1[0], self.player_1[1] - self.SPELL_COST)

    def check_if_shield_is_possible(self):

        if self.player_1[1] >= self.SPELL_COST:

            entities = []

            for hero in self.heroes:

                if hero.shield_life == 0 and hero.is_controlled == 1:
                    entities.append(hero)

            for entity in entities:
                if self.player_1[1] >= self.SPELL_COST:
                    self.shield(entity.id)

    def do_random_move(self):

        move_is_ok = False
        compteur = 0
        while not move_is_ok:

            x = random.randint(-100, 100)
            y = random.randint(-100, 100)

            if x != 0 and y != 0:
                futur_position = self.position + (vector(x, y).get_unit_vector() * 400)
                futur_position = futur_position.int()

                position_check = 0 < futur_position.x < 17630 and 0 < futur_position.y < 9000
                circle_check = self.check_point_on_circle(futur_position, self.base_coordonate, 6200)

                move_is_ok = position_check and circle_check
            compteur += 1
            if compteur > 100:
                break
        self.move(futur_position.x, futur_position.y)