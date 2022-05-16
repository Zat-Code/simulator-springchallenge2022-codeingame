import cv2
import numpy as np
from src.simulator.config.config import Config


class Render:

    def __init__(self, player_1, player_2, monsters):

        self.config = Config()

        self.player_1 = player_1
        self.player_2 = player_2
        self.monsters = monsters

        self.ratio = 10

        self.color_player_1 = (255, 0, 0)
        self.color_player_2 = (0, 0, 255)
        self.color_mob = (0, 0, 0)

        self.color_base = (0, 139, 255)

        self.color_view_player_1 = (255, 226, 212)
        self.color_view_player_2 = (212, 228, 255)

        self.color_wind = (255, 255, 255)

    def generate_image(self):

        self.img = np.full((int(self.config.MAP_HEIGHT/10), int(self.config.MAP_WIDTH/10), 3), (190, 190, 190), np.uint8)

        self.draw_view_for_each_player()
        self.draw_base()
        self.draw_monster()
        self.draw_heroes()
        self.draw_score()

    def draw_view_for_each_player(self):

        for heroes in self.player_1.heroes.heroes:
            reduce_position = (heroes.position/10).int()
            cv2.circle(self.img, (reduce_position.x, reduce_position.y), int(self.config.HERO_VIEW_RADIUS/10), self.color_view_player_1, -1)

        for heroes in self.player_2.heroes.heroes:
            reduce_position = (heroes.position/10).int()
            cv2.circle(self.img, (reduce_position.x, reduce_position.y), int(self.config.HERO_VIEW_RADIUS/10), self.color_view_player_2, -1)

        base1 = self.player_1.base
        cv2.circle(self.img, (base1.position.x, base1.position.y), int(self.config.BASE_VIEW_RADIUS / 10), self.color_view_player_1, -1)

        base2 = self.player_2.base
        reduce_position = (base2.position/10).int()
        cv2.circle(self.img, (reduce_position.x, reduce_position.y), 600, self.color_view_player_2, -1)



    def draw_monster(self):

        for monster in self.monsters.monsters:

            reduce_position = (monster.position/10).int()

            if monster.threat_for == 0:
                cv2.circle(self.img, (reduce_position.x, reduce_position.y), 10, self.color_mob, -1)
            else:
                cv2.circle(self.img, (reduce_position.x, reduce_position.y), 10, (0, 255, 0), -1)

            futur_position = ((monster.position + (monster.trajectory.get_unit_vector() * monster.velocity))/10).int()

            cv2.line(self.img, (reduce_position.x,  reduce_position.y), (futur_position.x, futur_position.y), self.color_mob, 1)

            if monster.shield_life != 0:
                cv2.circle(self.img, (reduce_position.x, reduce_position.y), 20, (240, 255, 0), 5)

            if monster.is_controlled == 1:
                cv2.circle(self.img, (reduce_position.x, reduce_position.y), 20, (0, 255, 240), 5)

            cv2.putText(self.img, str(monster.health), (reduce_position.x, reduce_position.y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)

    def draw_heroes(self):

        for heroes in self.player_1.heroes.heroes:

            reduce_position = (heroes.position/10).int()
            cv2.circle(self.img, (reduce_position.x, reduce_position.y), int(self.config.HEROES_ATTACK_RANGE/10), self.color_player_1)
            cv2.circle(self.img, (reduce_position.x, reduce_position.y), 10, self.color_player_1, -1)

            if heroes.shield_life != 0:
                cv2.circle(self.img, (reduce_position.x, reduce_position.y), 20, (240, 255, 0), 5)

            if heroes.is_controlled == 1:
                cv2.circle(self.img, (reduce_position.x, reduce_position.y), 20, (0, 255, 240), 5)

            if heroes.wind_trajectory:
                reduce_wind_trajectory = (heroes.wind_trajectory/10).int()
                cv2.line(self.img, (reduce_position.x,  reduce_position.y), (reduce_position.x + reduce_wind_trajectory.x, reduce_position.y + reduce_wind_trajectory.y), self.color_wind, 1)
                heroes.wind_trajectory = None

        for heroes in self.player_2.heroes.heroes:

            reduce_position = (heroes.position/10).int()
            cv2.circle(self.img, (reduce_position.x, reduce_position.y), int(self.config.HEROES_ATTACK_RANGE/10), self.color_player_2)
            cv2.circle(self.img, (reduce_position.x, reduce_position.y), 10, self.color_player_2, -1)

            if heroes.shield_life != 0:
                cv2.circle(self.img, (reduce_position.x, reduce_position.y), 20, (240, 255, 0), 5)

            if heroes.is_controlled == 1:
                cv2.circle(self.img, (reduce_position.x, reduce_position.y), 20, (0, 255, 240), 5)

            if heroes.wind_trajectory:
                reduce_wind_trajectory = (heroes.wind_trajectory/10).int()
                cv2.line(self.img, (reduce_position.x,  reduce_position.y), (reduce_position.x + reduce_wind_trajectory.x, reduce_position.y + reduce_wind_trajectory.y), self.color_wind, 1)
                heroes.wind_trajectory = None

    def draw_base(self):

        base1 = self.player_1.base
        cv2.circle(self.img, (base1.position.x, base1.position.y), int(self.config.BASE_ATTRACTION_RADIUS / 10), self.color_base, -1)
        cv2.circle(self.img, (base1.position.x, base1.position.y), int(self.config.BASE_RADIUS / 10), self.color_player_1, -1)

        base2 = self.player_2.base
        reduce_position = (base2.position/10).int()
        cv2.circle(self.img, (reduce_position.x, reduce_position.y), int(self.config.BASE_ATTRACTION_RADIUS / 10), self.color_base, -1)
        cv2.circle(self.img, (reduce_position.x, reduce_position.y), int(self.config.BASE_RADIUS / 10),  self.color_player_2, -1)

    def draw_score(self):

        width_render = int(self.config.MAP_WIDTH/10)

        score = np.full((50, width_render, 3), (255, 255, 255), np.uint8)

        self.img = np.concatenate((score, self.img), axis=0)


        cv2.putText(self.img, "PLAYER 1", (10, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1, cv2.LINE_AA)

        cv2.putText(self.img, str(self.player_1.life), (180, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)

        cv2.putText(self.img, str(self.player_1.mana), (210, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1, cv2.LINE_AA)

        cv2.putText(self.img, "PLAYER 2", (290, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1, cv2.LINE_AA)

        cv2.putText(self.img, str(self.player_2.life), (460, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)

        cv2.putText(self.img, str(self.player_2.mana), (490, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1, cv2.LINE_AA)


    def render(self):

        self.generate_image()
        cv2.imshow("game", self.img)
        key = cv2.waitKey(0)

        if key == ord('d'):
            pass