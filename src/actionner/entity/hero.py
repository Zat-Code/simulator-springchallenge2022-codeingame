from src.simulator.entity.character import Character
from src.utils.vector import vector


class Hero(Character):

    def __init__(self, x, y, id, type_character, shield_life, is_controlled, health, vx, vy, near_base, threat_for, monsters, base_coordonate, player_1, player_2, turn, get_print=None):

        super().__init__(x, y, id, type_character, shield_life, is_controlled, health, vx, vy, near_base, threat_for, 800)

        self.get_print = get_print

        self.SPELL_WIND_RADIUS = 1280
        self.SPELL_CONTROL_RADIUS = 2200
        self.SPELL_COST = 10

        self.action = None

        self.monsters = monsters
        self.heroes_ennemy = None
        self.heroes = None
        self.base_coordonate = base_coordonate
        self.player_1 = player_1
        self.player_2 = player_2
        self.turn = turn

    def set_heroes(self, heroes_ennemy, heroes):

        self.heroes_ennemy = heroes_ennemy
        self.heroes = heroes

    def move(self, x, y):

        x = int(x)
        y = int(y)

        self.action = "MOVE {} {}".format(x, y)

    def wait(self):

        self.action = "WAIT"

    def wind(self, trajectory):

        self.action = "SPELL WIND {} {}".format(int(trajectory.x), int(trajectory.y))

    def shield(self, id):

        self.action = "SPELL SHIELD {}".format(id)

    def control(self, id, trajectory):
        self.action = "SPELL CONTROL {} {} {}".format(id, int(trajectory.x), int(trajectory.y))

    def do_action(self):

        if self.get_print == None:
            print(self.action)
        else:
            print(self.action, file=self.get_print)


    def process_distance_hero2base(self, base_position):

        self.distance_hero2base = vector(base_position, self.position).norm(int_format=True)
        return self.distance_hero2base

    def check_if_monster_is_in_wind_range(self, monster):

        if self.check_point_on_circle(monster.position, self.position, self.SPELL_WIND_RADIUS):
            return 1
        else:
            return 0

    def check_if_monster_is_in_control_and_shield_range(self, monster):

        if self.check_point_on_circle(monster.position, self.position, self.SPELL_CONTROL_RADIUS):
            return 1
        else:
            return 0

    def check_point_on_circle(self, point, center, radius):
        return (point.x - center.x) ** 2 + (point.y - center.y) ** 2 <= radius ** 2
