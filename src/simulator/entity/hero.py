from src.simulator.entity.character import Character
from src.utils.vector import vector

class Hero(Character):

    def __init__(self, x, y, id, type_character, shield_life, is_controlled, health, vx, vy, near_base, threat_for,  player):

        super().__init__(x, y, id, type_character, shield_life, is_controlled, health, vx, vy, near_base, threat_for, 800)

        self.player = player
        self.wind_trajectory = None

    def move(self, action):

        x = int(action[1])
        y = int(action[2])

        diff = vector(x - self.position.x, y - self.position.y)

        # if diff.norm() > 500:
        if self.is_controlled == 0:
            self.change_trajectory(vector(x, y))

        mouvement = self.trajectory.get_unit_vector() * self.velocity
        self.move_character(mouvement.x, mouvement.y)

        self.is_controlled = 0

    def spell(self, action, monsters, heroes_player_1, heroes_player_2):

        name_spell = action[1]

        if name_spell == "WIND":

            x = action[2]
            y = action[3]

            if self.player.mana >= self.config.SPELL_WIND_COST:
                self.wind(int(x), int(y), monsters, heroes_player_2)
                self.player.mana -= self.config.SPELL_WIND_COST

        if name_spell == "SHIELD":

            id = action[2]

            if self.player.mana >= self.config.SPELL_WIND_COST:
                self.shield(id, monsters, heroes_player_1)
                self.player.mana -= self.config.SPELL_WIND_COST

        if name_spell == "CONTROL":

            id = int(action[2])
            x = int(action[3])
            y = int(action[4])

            if self.player.mana >= self.config.SPELL_WIND_COST:
                self.control(id, x, y, monsters, heroes_player_2)
                self.player.mana -= self.config.SPELL_CONTROL_COST

    def check_if_monster_is_in_attack_range(self, monster):

        if self.check_point_on_circle(monster.position, self.position, self.config.HEROES_ATTACK_RANGE):
            monster.get_damage()
            self.player.mana += 1
            self.player.max_mana += 1

    def check_if_monster_is_in_view_radius(self, monster):

        if self.type == 1:
            if self.check_point_on_circle(monster.position, self.position, self.config.HERO_VIEW_RADIUS):
                monster.see_per_heroes_player_1 += 1

        elif self.type == 2:
            if self.check_point_on_circle(monster.position, self.position, self.config.HERO_VIEW_RADIUS):
                monster.see_per_heroes_player_2 += 1

    def wind(self, x, y, monsters, heroes_player_2):

        if self.player.player_id == 1:
            self.wind_trajectory = vector(x, y).get_unit_vector() * self.config.SPELL_WIND_DISTANCE
        else:
            self.wind_trajectory = vector(x, y).inv().get_unit_vector() * self.config.SPELL_WIND_DISTANCE

        for monster in monsters:
            if monster.shield_life == 0:
                if self.check_point_on_circle(monster.position, self.position, self.config.SPELL_WIND_RADIUS):
                    monster.position = (monster.position + self.wind_trajectory).int()

        for hero in heroes_player_2:
            if hero.shield_life == 0:
                if self.check_point_on_circle(hero.position, self.position, self.config.SPELL_WIND_RADIUS):
                    hero.position = (hero.position + self.wind_trajectory).int()

    def shield(self, id_entity, monsters, heroes_player_1):

        monster_index = [i for i, monster in enumerate(monsters) if monster.id == int(id_entity)]
        heroes_index = [i for i, hero in enumerate(heroes_player_1) if hero.id == int(id_entity)]

        if len(monster_index) > 0:
            if monsters[monster_index[0]].shield_life == 0:
                monsters[monster_index[0]].shield_life = 12
        if len(heroes_index) > 0:
            if heroes_player_1[heroes_index[0]].shield_life == 0:
                heroes_player_1[heroes_index[0]].shield_life = 12

    def control(self, id_entity, x, y,  monsters, heroes_player_2):

        monster_index = [i for i, monster in enumerate(monsters) if monster.id == int(id_entity)]
        heroes_index = [i for i, hero in enumerate(heroes_player_2) if hero.id == int(id_entity)]

        if len(monster_index) > 0:
            if monsters[monster_index[0]].shield_life == 0:
                monsters[monster_index[0]].is_controlled = 1
                monsters[monster_index[0]].change_trajectory(vector(int(x), int(y)))

        if len(heroes_index) > 0:
            if heroes_player_2[heroes_index[0]].shield_life == 0:
                heroes_player_2[heroes_index[0]].is_controlled = 1
                heroes_player_2[heroes_index[0]].change_trajectory(vector(int(x), int(y)))

    def check_point_on_circle(self, point, center, radius):
        return (point.x - center.x) ** 2 + (point.y - center.y) ** 2 <= radius ** 2

    def change_trajectory(self, coordonate):

        self.trajectory = vector(self.position, coordonate).get_unit_vector()