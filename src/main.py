from simulator.engine.engine import Engine
from simulator.render.render import Render
from simulator.parser.parse_object_to_list import ParseObjectToList
from src.actionner.actionner import Actionner
from src.simulator.config.config import Config
from itertools import combinations_with_replacement, product
import json
import time


class Main:


    def __init__(self):

        self.config = Config()

        self.class_possible = [0, 1, 2, 3, 4, 5]

        self.combination_possible = product(self.class_possible, repeat=3)
        self.combination_possible_2 = product(self.class_possible, repeat=3)


    def run_all_composition(self):

        dict_result = {}

        for composition in self.combination_possible:
            print('##################')
            key_composition = ''
            for hero in composition:
                key_composition += str(hero)
                dict_result[key_composition] = {}

            for composition_ennemy in self.combination_possible_2:
                key_ennemy = ''
                for ennemy in composition_ennemy:
                    key_ennemy += str(ennemy)
                    dict_result[key_composition][key_ennemy] = {}

                win_player_1 = 0
                win_player_2 = 0
                draw = 0
                error = 0

                for i in range(0, 100):
                    # print("Next game {}".format(i))
                    try:
                        ret = self.run_one_game_without_render(composition, composition_ennemy)
                    except:
                        ret = -10

                    if ret == 1:
                        win_player_1 += 1
                    elif ret == 2:
                        win_player_2 += 1
                    elif ret == -10:
                        error += 1
                    else:
                        draw += 1

                dict_result[key_composition][key_ennemy] = {'win_player_1': win_player_1, 'win_player_2': win_player_2, 'draw': draw, 'error': error}
                print("{} vs {} : player 1 {} % win, player 2 {} % win, draw {} %".format(composition, composition_ennemy, win_player_1, win_player_2, draw))

            # print(win_player_1, win_player_2, draw)
            with open('result.json', 'w') as outfile:
                json.dump(dict_result, outfile, indent=4)

    def run_one_game_with_render(self, class_hero_player_1, class_hero_player_2):
        engine = Engine()
        base_player_1 = engine.player_1.base.position
        base_player_2 = engine.player_2.base.position

        for i in range(0, self.config.MAX_TURN):

            print("########  TURN {} ########".format(i))
            ret = engine.run()

            render = Render(engine.player_1, engine.player_2, engine.monsters)
            render.render()

            parser = ParseObjectToList(engine.player_1, engine.player_2, engine.monsters)
            print('## player 1 ##')
            player_1, player_2, entity_count, entity = parser.parse_for_player_1()
            actionner_player_1 = Actionner(base_player_1, player_1, player_2, entity, i, class_hero_player_1, engine.get_print)
            print('## player 2 ##')
            player_1, player_2, entity_count, entity = parser.parse_for_player_2()
            actionner_player_2 = Actionner(base_player_2, player_2, player_1, entity, i, class_hero_player_2,  engine.get_print)

            if ret != 0:
                break

        if ret == -1:
            if engine.player_1.max_mana > engine.player_2.max_mana:
                ret = 1
                # print("victoire mana player1 : {} {}".format(engine.player_1.max_mana, engine.player_2.max_mana))
            elif engine.player_1.max_mana < engine.player_2.max_mana:
                ret = 2
                # print("victoire mana player2 : {} {}".format(engine.player_1.max_mana, engine.player_2.max_mana))
            else:
                ret = -1

        return ret

    def run_one_game_without_render(self, class_hero_player_1, class_hero_player_2):
        engine = Engine()
        base_player_1 = engine.player_1.base.position
        base_player_2 = engine.player_2.base.position

        for i in range(0, self.config.MAX_TURN):

            # print("########  TURN {} ########".format(i))
            ret = engine.run()

            # render = Render(engine.player_1, engine.player_2, engine.monsters)
            # render.render()

            parser = ParseObjectToList(engine.player_1, engine.player_2, engine.monsters)

            player_1, player_2, entity_count, entity = parser.parse_for_player_1()
            actionner_player_1 = Actionner(base_player_1, player_1, player_2, entity, i, class_hero_player_1, engine.get_print)

            player_1, player_2, entity_count, entity = parser.parse_for_player_2()
            actionner_player_2 = Actionner(base_player_2, player_2, player_1, entity, i, class_hero_player_2, engine.get_print)

            if ret != 0:
                break

        if ret == -1:

            if engine.player_1.life > engine.player_2.life:
                ret = 1
            elif engine.player_1.life < engine.player_2.life:
                ret = 2
            elif engine.player_1.life == engine.player_2.life:

                if engine.player_1.max_mana > engine.player_2.max_mana:
                    ret = 1
                    # print("victoire mana player1 : {} {}".format(engine.player_1.max_mana, engine.player_2.max_mana))
                elif engine.player_1.max_mana < engine.player_2.max_mana:
                    ret = 2
                    # print("victoire mana player2 : {} {}".format(engine.player_1.max_mana, engine.player_2.max_mana))
                else:
                    ret = -1

        return ret

    def run_one_composition(self, class_hero_player_1):

        dict_result = {}

        combination_possible = list(combinations_with_replacement(self.class_possible, 6))


        key_composition = ''
        for hero in class_hero_player_1:
            key_composition += str(hero)
            dict_result[key_composition] = {}

        for composition_ennemy in combination_possible:
            key_ennemy = ''
            for ennemy in composition_ennemy:
                key_ennemy += str(ennemy)
                dict_result[key_composition][key_ennemy] = {}

            win_player_1 = 0
            win_player_2 = 0
            draw = 0
            error = 0

            for i in range(0, 100):
                # print("Next game {}".format(i))
                try:
                    ret = self.run_one_game_without_render(class_hero_player_1, composition_ennemy)
                except:
                    ret = -10

                if ret == 1:
                    win_player_1 += 1
                elif ret == 2:
                    win_player_2 += 1
                elif ret == -10:
                    error += 1
                else:
                    draw += 1

            dict_result[key_composition][key_ennemy] = {'win_player_1': win_player_1, 'win_player_2': win_player_2,
                                                        'draw': draw, 'error': error}
            print("{} vs {} : player 1 {} % win, player 2 {} % win, draw {} %".format(class_hero_player_1, composition_ennemy,
                                                                                      win_player_1, win_player_2, draw))


        with open(r'E:\Dev\simulator-springchallenge2022-codeingame\data/{}.json'.format(key_composition), 'w') as outfile:
            json.dump(dict_result, outfile, indent=4)

    def run_with_two_composition(self, class_hero_player_1, composition_ennemy):


        win_player_1 = 0
        win_player_2 = 0
        draw = 0
        error = 0

        for i in range(0, 100):
            # print("Next game {}".format(i))
            # try:
            ret = self.run_one_game_without_render(class_hero_player_1, composition_ennemy)
            # except:
            #     ret = -10

            if ret == 1:
                win_player_1 += 1
            elif ret == 2:
                win_player_2 += 1
            elif ret == -10:
                error += 1
            else:
                draw += 1

        print("{} vs {} : player 1 {} % win, player 2 {} % win, draw {} %".format(class_hero_player_1, composition_ennemy,
                                                                                  win_player_1, win_player_2, draw))

    def run_100_game_with_render(self, class_hero_player_1, composition_ennemy):

        dict_result = {}


        win_player_1 = 0
        win_player_2 = 0
        draw = 0
        error = 0

        for i in range(0, 100):
            print("Next game {}".format(i))
            try:
                ret = self.run_one_game_without_render(composition, composition_ennemy)
            except:
                ret = -10

            if ret == 1:
                win_player_1 += 1
            elif ret == 2:
                win_player_2 += 1
            elif ret == -10:
                error += 1
            else:
                draw += 1

        print("{} vs {} : player 1 {} % win, player 2 {} % win, draw {} %".format(composition, composition_ennemy,
                                                                                win_player_1, win_player_2,
                                                                                draw))


if __name__ == '__main__':

    main = Main()

    composition = [4, 4, 5, 4, 0, 4,  4, 3, 4]
    composition_ennemy = [4, 4, 5, 4, 0, 4,  4, 3, 4]
    #(0, 3, 3, 4, 5, 5)
    # main.run_one_composition(composition)
    # main.run_one_game_with_render(composition, composition_ennemy)
    main.run_100_game_with_render(composition, composition_ennemy)
    # main.run_with_two_composition(composition, composition_ennemy)