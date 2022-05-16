from src.actionner.entity.hero import Hero
from src.utils.vector import vector
import random



class DefenserControlMob(Hero):

    def __init__(self,  x, y, id, type_character, shield_life, is_controlled, health, vx, vy, near_base, threat_for, monsters, base_coordonate, player_1, player_2, turn, get_print=None):
        super().__init__(x, y, id, type_character, shield_life, is_controlled, health, vx, vy, near_base, threat_for, monsters, base_coordonate, player_1, player_2, turn, get_print=get_print)

        if self.base_coordonate.x == 0:
            self.base_coordonate_ennemy = vector(17630, 9000)
        else:
            self.base_coordonate_ennemy = vector(0, 0)

    def run(self):

        self.check_near_monster()

        if not(self.check_point_on_circle(self.position, self.base_coordonate, 10000)) or self.check_point_on_circle(self.position, self.base_coordonate, 7000):
            self.move(int(17630/2), int(9000/2))

        self.check_if_control_is_possible()


    def check_near_monster(self):

        for monster in self.monsters:
            monster.process_distance_monster2base(self.base_coordonate_ennemy)

        monsters_sort = self.monsters.copy()

        monsters_sort.sort(key=lambda monster: monster.distance_monster2base)

        monster_find = False
        for monster in monsters_sort:
                if vector(self.base_coordonate, monster.position).norm(int_format=True) > 6000 and monster.threat_for == 1:
                    self.move(monster.position.x, monster.position.y)
                    monster.is_cibled = 1
                    monster_find = True
                    break
        if not monster_find:
            if not monster_find:
                if len(monsters_sort) == 0:
                    self.wait()
                else:
                    self.move(monsters_sort[0].position.x, monsters_sort[0].position.y)
            # self.do_random_move()

    def check_if_control_is_possible(self):

        if self.player_1[1] >= self.SPELL_COST:

            entities = []

            nb_monster_in_wind = 0
            monster_in_wind = []
            for monster in self.monsters:

                ret = self.check_if_monster_is_in_control_and_shield_range(monster)
                nb_monster_in_wind += ret

                if ret == 1 and monster.threat_for == 1:
                    monster_in_wind.append(monster)
                    entities.append([nb_monster_in_wind, monster_in_wind])

            for entity in entities:
                if self.player_1[1] >= self.SPELL_COST:
                    if entity[0] > 0:

                        self.control(entity[1][0].id, vector(self.base_coordonate_ennemy.x+random.randint(-100, 100), self.base_coordonate_ennemy.y+random.randint(-100, 100)))
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
                circle_check = self.check_point_on_circle(self.position, self.base_coordonate, 9000) or not(self.check_point_on_circle(self.position, self.base_coordonate, 7000))

                print(self.check_point_on_circle(self.position, self.base_coordonate, 9000), not(self.check_point_on_circle(self.position, self.base_coordonate, 7000)))

                move_is_ok = position_check and circle_check
            compteur += 1
            if compteur > 100:
                break
        self.move(futur_position.x, futur_position.y)