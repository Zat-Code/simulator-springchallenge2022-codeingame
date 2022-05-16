from src.simulator.config.config import Config


class Base:

    def __init__(self, player, position):

        self.player = player

        self.position = position
        self.config = Config()

    def check_if_monster_is_in_base_attraction_radius(self, monster):

        if monster.is_controlled == 0:
            result = self.check_point_on_circle(monster.position, self.position, self.config.BASE_ATTRACTION_RADIUS)
            if result:
                monster.change_trajectory(self.position)
                monster.near_base = self.player.player_id

    def check_if_monster_is_in_base(self, monster):

        result = self.check_point_on_circle(monster.position, self.position, self.config.BASE_RADIUS)
        if result:
            self.player.take_damage()
            monster.destroy()

    def check_if_monster_is_in_view_radius(self, monster):

        if self.player.player_id == 1:
            if self.check_point_on_circle(monster.position, self.position, self.config.BASE_VIEW_RADIUS):
                monster.see_per_base_player_1 += 1

        elif self.player.player_id == 2:
            if self.check_point_on_circle(monster.position, self.position, self.config.BASE_VIEW_RADIUS):
                monster.see_per_base_player_2 += 1


    def check_if_monster_can_be_in_base(self, monster):

        monster.test_threat_for(self)

        # vector_threat_for = monster.calcul_vector_threat_for(self)
        # result = self.check_point_on_circle(vector_threat_for, self.position, self.config.BASE_RADIUS)
        #
        # if result:
        #     monster.threat_for = self.player.player_id
        # else:
        #     monster.threat_for = 0

    def check_point_on_circle(self, point, center, radius):
        return (point.x - center.x) ** 2 + (point.y - center.y) ** 2 <= radius ** 2