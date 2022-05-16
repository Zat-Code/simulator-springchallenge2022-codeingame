from src.simulator.config.config import Config
from src.simulator.group.heroes import Heroes
from src.simulator.entity.base import Base
from src.utils.vector import vector


class Player:
    def __init__(self, player_id):

        self.config = Config()

        self.player_id = player_id

        self.life = self.config.STARTING_BASE_LIFE
        self.mana = self.config.STARTING_MANA

        self.max_mana = self.config.STARTING_MANA

        self.heroes = Heroes(self.player_id, self)

        if self.player_id == 1:
            self.base = Base(self, vector(0, 0))
        else:
            self.base = Base(self, vector(self.config.MAP_WIDTH, self.config.MAP_HEIGHT))

    def is_dead(self):

        if self.life <= 0:
            return True
        else:
            return False

    def take_damage(self):

        self.life -= 1
        # print("player {} take damage, life {}".format(self.player_id, self.life))

    def do_view_player(self, monsters):

        for monster in monsters:

            self.base.check_if_monster_is_in_view_radius(monster)
            self.base.check_if_monster_is_in_base_attraction_radius(monster)
            self.base.check_if_monster_is_in_base(monster)
            self.base.check_if_monster_can_be_in_base(monster)

            for hero in self.heroes.heroes:
                hero.check_if_monster_is_in_view_radius(monster)

    def do_attack_hero(self, monsters):

        for monster in monsters:
            for hero in self.heroes.heroes:
                hero.check_if_monster_is_in_attack_range(monster)
