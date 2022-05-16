from src.simulator.entity.character import Character
from src.utils.vector import vector
import numpy as np


class Monster(Character):

    def __init__(self, x, y, id, type_character, shield_life, is_controlled, health, vx, vy, near_base, threat_for):

        super().__init__(x, y, id, type_character, shield_life, is_controlled, health, vx, vy, near_base, threat_for,
                         400)

        self.alive = True
        self.see_per_heroes_player_1 = 0
        self.see_per_heroes_player_2 = 0

        self.see_per_base_player_1 = 0
        self.see_per_base_player_2 = 0

        self.p2 = vector(0, 0)

    def move(self):

        mouvement = self.trajectory.get_unit_vector() * self.velocity
        self.move_character(mouvement.x, mouvement.y)

        self.is_controlled = 0

        self.see_per_heroes_player_1 = 0
        self.see_per_heroes_player_2 = 0

        self.see_per_base_player_1 = 0
        self.see_per_base_player_2 = 0

    def change_trajectory(self, position_base):

        self.trajectory = vector(self.position, position_base).get_unit_vector()

    def get_damage(self):

        self.health -= self.config.HERO_ATTACK_DAMAGE

        if self.health <= 0:
            self.alive = False

    def test_threat_for(self, base):


        # intersect1 = self.calcul_intersection(base.position, base.position + vector(6000, 0), self.position, self.position + self.trajectory)
        # intersect2 = self.calcul_intersection(base.position, base.position + vector(0, 6000), self.position, self.position + self.trajectory)

        p2 = self.position + (self.trajectory)
        try:
            intersect = self.circle_line_segment_intersection((base.position.x, base.position.y), self.config.BASE_ATTRACTION_RADIUS, (self.position.x, self.position.y), (p2.x, p2.y))
        except:
            intersect = []

        if intersect != []:
            check = True
        else:
            check = False


        if check:
            self.threat_for = base.player.player_id


    def calcul_intersection(self, base_position, base_lenght, monster_position, monster_position_and_trajectory):

        L1 = self.line(base_position, base_position + base_lenght)
        L2 = self.line(monster_position, monster_position_and_trajectory)
        #
        R = self.intersection(L1, L2)

        check = False
        if R:
            for i, element in enumerate(R):

                if element != 0:
                    if i == 0:
                        if base_position.x < element < base_position.x + base_lenght.x:
                            check = True
                    else:
                        if base_position.y < element < base_position.y + base_lenght.y:
                            check = True
        print(check)
        return R

    def circle_line_segment_intersection(self, circle_center, circle_radius, pt1, pt2, full_line=True, tangent_tol=1e-9):
        """ Find the points at which a circle intersects a line-segment.  This can happen at 0, 1, or 2 points.

        :param circle_center: The (x, y) location of the circle center
        :param circle_radius: The radius of the circle
        :param pt1: The (x, y) location of the first point of the segment
        :param pt2: The (x, y) location of the second point of the segment
        :param full_line: True to find intersections along full line - not just in the segment.  False will just return intersections within the segment.
        :param tangent_tol: Numerical tolerance at which we decide the intersections are close enough to consider it a tangent
        :return Sequence[Tuple[float, float]]: A list of length 0, 1, or 2, where each element is a point at which the circle intercepts a line segment.

        Note: We follow: http://mathworld.wolfram.com/Circle-LineIntersection.html
        """

        (p1x, p1y), (p2x, p2y), (cx, cy) = pt1, pt2, circle_center
        (x1, y1), (x2, y2) = (p1x - cx, p1y - cy), (p2x - cx, p2y - cy)
        dx, dy = (x2 - x1), (y2 - y1)
        dr = (dx ** 2 + dy ** 2) ** .5
        big_d = x1 * y2 - x2 * y1
        discriminant = circle_radius ** 2 * dr ** 2 - big_d ** 2

        if discriminant < 0:  # No intersection between circle and line
            return []
        else:  # There may be 0, 1, or 2 intersections with the segment
            intersections = [
                (cx + (big_d * dy + sign * (-1 if dy < 0 else 1) * dx * discriminant ** .5) / dr ** 2,
                 cy + (-big_d * dx + sign * abs(dy) * discriminant ** .5) / dr ** 2)
                for sign in ((1, -1) if dy < 0 else (-1, 1))]  # This makes sure the order along the segment is correct
            if not full_line:  # If only considering the segment, filter out intersections that do not fall within the segment
                fraction_along_segment = [(xi - p1x) / dx if abs(dx) > abs(dy) else (yi - p1y) / dy for xi, yi in
                                          intersections]
                intersections = [pt for pt, frac in zip(intersections, fraction_along_segment) if 0 <= frac <= 1]
            if len(intersections) == 2 and abs(
                    discriminant) <= tangent_tol:  # If line is tangent to circle, return just one point (as both intersections have same location)
                return [intersections[0]]
            else:
                return intersections

    def destroy(self):
        self.alive = False

    def line(self, p1, p2):
        A = (p1.y - p2.y)
        B = (p2.x - p1.x)
        C = (p1.x * p2.y - p2.x * p1.y)
        return A, B, -C

    def intersection(self, L1, L2):
        D = L1[0] * L2[1] - L1[1] * L2[0]
        Dx = L1[2] * L2[1] - L1[1] * L2[2]
        Dy = L1[0] * L2[2] - L1[2] * L2[0]
        if D != 0:
            x = Dx / D
            y = Dy / D
            return [int(x), int(y)]
        else:
            return False
