from src.actionner.entity.hero import Hero
from src.utils.vector import vector
import random


class Farmer(Hero):

    def __init__(self,  x, y, id, type_character, shield_life, is_controlled, health, vx, vy, near_base, threat_for, monsters, base_coordonate, player_1, player_2, turn, get_print=None):
        super().__init__(x, y, id, type_character, shield_life, is_controlled, health, vx, vy, near_base, threat_for, monsters, base_coordonate, player_1, player_2, turn, get_print=get_print)


    def run(self):


        self.check_near_monster()

        if not (
        self.check_point_on_circle(self.position, self.base_coordonate, 10000)) or self.check_point_on_circle(
                self.position, self.base_coordonate, 7000):
            self.move(int(17630 / 2), int(9000 / 2))
            # self.check_if_control_is_possible()

    def check_near_monster(self):

        for monster in self.monsters:
            monster.process_distance_monster2hero(self.position)

        monsters_sort = self.monsters.copy()

        monsters_sort.sort(key=lambda monster: monster.distance_monster2hero)

        monster_find = False
        for monster in monsters_sort:

            self.move(monster.position.x, monster.position.y)
            monster.is_cibled = 1
            monster_find = True
            break

        if not monster_find:
            if not monster_find:
                if len(monsters_sort) == 0:
                    self.wait()
                    # self.do_random_move()
                else:
                    if 0 < monsters_sort[0].position.x < 17630 and 0 < monsters_sort[0].position.y < 9000:
                        self.move(monsters_sort[0].position.x, monsters_sort[0].position.y)
                    else:
                        self.wait()

    def do_random_move(self):

        move_is_ok = False
        compteur = 0
        while not move_is_ok:

            x = random.randint(-100, 100)
            y = random.randint(-100, 100)

            if x != 0 and y != 0:
                futur_position = self.position + (vector(x, y).get_unit_vector() * 800)
                futur_position = futur_position.int()

                position_check = 0 < futur_position.x < 17630 and 0 < futur_position.y < 9000

                move_is_ok = position_check
            compteur += 1
            if compteur > 100:
                break
        self.move(futur_position.x, futur_position.y)