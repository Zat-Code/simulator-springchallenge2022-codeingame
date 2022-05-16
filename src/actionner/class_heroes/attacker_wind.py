from src.actionner.entity.hero import Hero
from src.utils.vector import vector
import random


class AttackerWind(Hero):

    def __init__(self,  x, y, id, type_character, shield_life, is_controlled, health, vx, vy, near_base, threat_for, monsters, base_coordonate, player_1, player_2, turn, get_print=None):
        super().__init__(x, y, id, type_character, shield_life, is_controlled, health, vx, vy, near_base, threat_for, monsters, base_coordonate, player_1, player_2, turn, get_print=get_print)


        if self.base_coordonate.x == 0:
            self.base_coordonate_ennemy = vector(17630, 9000)
        else:
            self.base_coordonate_ennemy = vector(0, 0)

    def run(self):

        if not(self.check_point_on_circle(self.position, self.base_coordonate_ennemy, 6000)) or self.check_point_on_circle(self.position, self.base_coordonate_ennemy, 4000):
            self.move(self.base_coordonate_ennemy.x, self.base_coordonate_ennemy.y)

        else:
            self.do_random_move()
            self.check_if_wind_is_possible()

    def check_if_wind_is_possible(self):

        if self.player_1[1] >= self.SPELL_COST:

            entities = []

            nb_monster_in_wind = 0
            monster_in_wind = []
            for monster in self.monsters:

                if monster.shield_life == 0:

                    ret = self.check_if_monster_is_in_wind_range(monster)
                    nb_monster_in_wind += ret

                    if ret == 1:
                        monster_in_wind.append(monster)

                    entities.append([nb_monster_in_wind, monster_in_wind])

            for entity in entities:
                if self.player_1[1] >= self.SPELL_COST:
                    if entity[0] > 0:
                        sum_trajectory_monster = vector(0, 0)
                        for monster in entity[1]:
                            sum_trajectory_monster += monster.trajectory

                        mean_trajectory = (sum_trajectory_monster/len(entity[1])).int()
                        wind_trajectory = self.position + mean_trajectory.inv()
                        self.wind(wind_trajectory)

                        self.player_1 = (self.player_1[0], self.player_1[1] - self.SPELL_COST)

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