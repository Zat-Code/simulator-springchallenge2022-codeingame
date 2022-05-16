from src.simulator.entity.character import Character
from src.utils.vector import vector


class Monster(Character):

    def __init__(self, x, y, id, type_character, shield_life, is_controlled, health, vx, vy, near_base, threat_for):

        super().__init__(x, y, id, type_character, shield_life, is_controlled, health, vx, vy, near_base, threat_for, 400)

        self.alive = True

        self.distance_monster2base = 1000000
        self.distance_monster2hero = 1000000

        self.is_cibled = False

        self.number_monster_near = 0

    def process_distance_monster2base(self, base_position):

        self.distance_monster2base = vector(base_position, self.position).norm(int_format=True)


    def process_distance_monster2hero(self, hero_position):

        self.distance_monster2hero = vector(hero_position, self.position).norm(int_format=True)

    def process_distance_monster2monsters(self, monsters):

        for monster in monsters:
            if monster.threat_for == 2 and monster.id != self.id and monster.shield_life <2:
                distance = vector(monster.position, self.position).norm(int_format=True)
                if distance <= 1000:
                    self.number_monster_near += 1