from src.simulator.config.config import Config
from src.simulator.entity.monster import Monster
import random


class Monsters:

    def __init__(self):

        self.spawn_rate = 5
        self.monster_starting_max_heal = 10
        self.monster_growth_max_heal = 0.5
        self.nb_monster_spawn_for_each_player = 2

        self.current_id_character = 6

        self.config = Config()

        self.monsters = []

        self.last_spawn = -self.spawn_rate

        self.current_max_health = self.monster_starting_max_heal

        self.low_range_spawn = self.config.MAP_WIDTH/2 - self.config.SPAWN_RANGE
        self.hight_range_spawn = self.config.MAP_WIDTH/2 + self.config.SPAWN_RANGE

        self.turn = 0

    def launch_move_monster(self):

        for i, monster in enumerate(self.monsters):
            if not monster.alive:
                self.monsters.pop(i)

            monster.move()

    def launch_spawn_monster(self):

        if self.turn - self.last_spawn >= self.spawn_rate:
            self.last_spawn = self.turn
            self.spawn_monster()

        self.turn += 1

    def decremented_shield(self):

        for monster in self.monsters:
            if monster.shield_life != 0:
                monster.shield_life -= 1

    def spawn_monster(self):

        # print('SPAWN monster TOUR : {}'.format(self.turn))

        for _ in range(self.nb_monster_spawn_for_each_player):
            x_monster_1, y_monster_1, vx_monster_1, vy_monster_1 = self.generate_position_and_trajectory_for_one_monster()
            self.monsters.append(Monster(x_monster_1, y_monster_1, self.current_id_character, 0, 0, 0, self.current_max_health, vx_monster_1, vy_monster_1, 0, 0))

            self.current_id_character += 1

            x_monster_2, y_monster_2, vx_monster_2, vy_monster_2 = self.generate_symetric_monster(x_monster_1, vx_monster_1, vy_monster_1)
            self.monsters.append(Monster(x_monster_2, y_monster_2, self.current_id_character, 0, 0, 0, self.current_max_health, vx_monster_2, vy_monster_2, 0, 0))

            self.current_id_character += 1

        self.current_max_health += self.monster_growth_max_heal

    def generate_position_and_trajectory_for_one_monster(self):

        x_monster_1 = random.randint(self.low_range_spawn, self.hight_range_spawn)
        vy_monster_1 = random.randint(-100, 100)

        y_monster_1 = self.config.MAP_HEIGHT - 1 if vy_monster_1 < 0 else 0
        vx_monster_1 = random.randint(-100, 100)

        return x_monster_1, y_monster_1, vx_monster_1, vy_monster_1

    def generate_symetric_monster(self, x_monster_1, vx_monster_1, vy_monster_1):

        if x_monster_1 < self.config.MAP_WIDTH/2:
            x_monster_2 = self.config.MAP_WIDTH/2 + (self.config.MAP_WIDTH/2 - x_monster_1)
        else:
            x_monster_2 = self.config.MAP_WIDTH/2 - (x_monster_1 - self.config.MAP_WIDTH/2)

        vy_monster_2 = -vy_monster_1

        y_monster_2 = 0 if vy_monster_1 < 0 else self.config.MAP_HEIGHT - 1
        vx_monster_2 = - vx_monster_1

        return x_monster_2, y_monster_2, vx_monster_2, vy_monster_2