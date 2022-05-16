from src.simulator.config.config import Config
from src.simulator.group.monsters import Monsters
from src.simulator.entity.player import Player
from io import StringIO


class Engine:

    def __init__(self):

        self.config = Config()

        self.turn = 0

        self.player_1 = Player(1)
        self.player_2 = Player(2)

        self.monsters = Monsters()

        self.get_print = StringIO()

    def run(self):


        self.update()

        if self.player_1.is_dead() and self.player_2.is_dead():
            # print("DRAW")
            return -1

        if self.player_1.is_dead():
            # print("PLAYER 2 WINS !")
            return 2

        if self.player_2.is_dead():
            # print("PLAYER 1 WINS !")
            return 1

        return 0

    def update(self):

        actions_move_player_1, actions_wind_player_1, actions_control_player_1, actions_shield_player_1, actions_move_player_2, actions_wind_player_2, actions_control_player_2, actions_shield_player_2 = self.parse_get_print()

        self.player_1.do_view_player(self.monsters.monsters)
        self.player_2.do_view_player(self.monsters.monsters)

        #1 Hero move
        self.player_1.heroes.move(actions_move_player_1)
        self.player_2.heroes.move(actions_move_player_2)

        # 2 Hero attack
        self.player_1.do_attack_hero(self.monsters.monsters)
        self.player_2.do_attack_hero(self.monsters.monsters)

        #3 Wind
        self.player_2.heroes.wind(actions_wind_player_2, self.monsters.monsters, self.player_1.heroes.heroes)
        self.player_1.heroes.wind(actions_wind_player_1, self.monsters.monsters, self.player_2.heroes.heroes)

        #4 Move monsters
        self.monsters.launch_move_monster()

        self.player_1.do_view_player(self.monsters.monsters)
        self.player_2.do_view_player(self.monsters.monsters)

        #5 Decremented shield
        self.monsters.decremented_shield()
        self.player_1.heroes.decremented_shield()

        # 6 Spawn new monsters
        self.monsters.launch_spawn_monster()

        #7 Control
        self.player_2.heroes.control(actions_control_player_2, self.monsters.monsters, self.player_1.heroes.heroes)
        self.player_1.heroes.control(actions_control_player_1, self.monsters.monsters, self.player_2.heroes.heroes)
        # self.player_2.heroes.control(actions_control_player_2, self.monsters.monsters, self.player_1.heroes.heroes)

        #8 Shield
        self.player_1.heroes.shield(actions_shield_player_1, self.monsters.monsters, self.player_1.heroes.heroes)
        self.player_2.heroes.shield(actions_shield_player_2, self.monsters.monsters, self.player_2.heroes.heroes)


        self.turn += 1
        self.get_print = StringIO()


    def parse_get_print(self):

        actions = self.get_print.getvalue()

        actions_move_player_1 = []
        actions_wind_player_1 = []
        actions_control_player_1 = []
        actions_shield_player_1 = []

        actions_move_player_2 = []
        actions_wind_player_2 = []
        actions_control_player_2 = []
        actions_shield_player_2 = []

        if actions != "":
            actions = actions.split('\n')

            for i, action in enumerate(actions):
                action = action.split(' ')
                if i < 3:
                    if action[0] == "MOVE":
                        actions_move_player_1.append((i, action))
                        # self.player_1.heroes.heroes[i].move(action)
                    elif action[0] == "SPELL":
                        if action[1] == "WIND":
                            actions_wind_player_1.append((i, action))
                        elif action[1] == "CONTROL":
                            actions_control_player_1.append((i, action))
                        elif action[1] == "SHIELD":
                            actions_shield_player_1.append((i, action))

                        # self.player_1.heroes.heroes[i].spell(action, self.monsters.monsters, self.player_1.heroes.heroes, self.player_2.heroes.heroes)

                elif i < 6:
                    if action[0] == "MOVE":
                        actions_move_player_2.append((i-3, action))
                        # self.player_2.heroes.heroes[i-3].move(action)
                    elif action[0] == "SPELL":

                        if action[1] == "WIND":
                            actions_wind_player_2.append((i-3, action))
                        elif action[1] == "CONTROL":
                            actions_control_player_2.append((i-3, action))
                        elif action[1] == "SHIELD":
                            actions_shield_player_2.append((i-3, action))

                        # self.player_2.heroes.heroes[i-3].spell(action, self.monsters.monsters, self.player_1.heroes.heroes, self.player_2.heroes.heroes)

        self.get_print = StringIO()
        return actions_move_player_1, actions_wind_player_1, actions_control_player_1, actions_shield_player_1, actions_move_player_2, actions_wind_player_2, actions_control_player_2, actions_shield_player_2



