from src.simulator.entity.hero import Hero
from src.simulator.config.config import Config


class Heroes:

    def __init__(self,  player_id, player):

        self.player_id = player_id
        self.player = player
        self.config = Config()
        self.heroes = self.generate_heroes()

    def generate_heroes(self):

        heroes_player = []

        if self.player_id == 1:

            for i, position in enumerate(self.config.POSITION_START_HEROES_PLAYER_1):
                heroes_player.append(Hero(position.x, position.y, i, self.player_id, 0, 0, -1, -1, -1, -1, -1, self.player))

        else:
            for i, position in enumerate(self.config.POSITION_START_HEROES_PLAYER_2):
                heroes_player.append(Hero(position.x, position.y, i+3, self.player_id, 0, 0, -1, -1, -1, -1, -1, self.player))

        return heroes_player


    def move(self, actions):

        for action in actions:
            self.heroes[action[0]].move(action[1])

    def wind(self, actions, monsters, heroes_ennemy):
        for action in actions:
            self.heroes[action[0]].spell(action[1], monsters, self.heroes,
                                                 heroes_ennemy)

    def shield(self, actions, monsters, heroes_ennemy):
        for action in actions:
            self.heroes[action[0]].spell(action[1], monsters, self.heroes,
                                                 heroes_ennemy)

    def control(self, actions, monsters, heroes_ennemy):
        for action in actions:
            self.heroes[action[0]].spell(action[1], monsters, self.heroes,
                                                 heroes_ennemy)


    def decremented_shield(self):

        for hero in self.heroes:
            if hero.shield_life != 0:
                hero.shield_life -= 1