import math


class vector:

    def __init__(self, p1, p2=-100000):

        if p2 == -100000:
            self.x = p1[0]
            self.y = p1[1]

        elif isinstance(p1, vector) and isinstance(p2, vector):
            self.x = p2.x - p1.x
            self.y = p2.y - p1.y
        else:
            self.x = p1
            self.y = p2

    def norm(self, int_format=False):

        norm = math.sqrt(math.pow(self.x, 2) + math.pow(
            self.y, 2))
        if int_format:
            return int(norm)
        else:
            return norm

    def get_unit_vector(self):

        norm = self.norm()

        try:
            true_div = self.__truediv__(norm)
        except:
            true_div = vector(0, 0)

        return true_div

    def translate(self, vector_2):

        self.x += vector_2.x
        self.y += vector_2.y

    def create_new_vector_with_translation(self, vector_2):

        x = vector_2.x + self.x
        y = vector_2.y + self.y

        return vector(x, y)

    def int(self):

        self.x = int(self.x)
        self.y = int(self.y)

        return self

    def __add__(self, vector_2):

        x = self.x + vector_2.x
        y = self.y + vector_2.y
        return vector(x, y)

    def __sub__(self, vector_2):

        x = self.x - vector_2.x
        y = self.y - vector_2.y

        return vector(x, y)

    def __mul__(self, value):

        x = self.x * value
        y = self.y * value

        return vector(x, y)

    def __truediv__(self, value):

        x = self.x / value
        y = self.y / value

        return vector(x, y)

    def multiply(self, vector_2):

        x = self.x * vector_2.x
        y = self.y * vector_2.y

        return vector(x, y)

    def mean(self, vector_2):

        x = (self.x + vector_2.x)/2
        y = (self.y + vector_2.y)/2

        return vector(x, y)

    def bissectrices(self):

        vector_1 = vector(-self.y, self.x).get_unit_vector()
        vector_2 = vector(self.y, -self.x).get_unit_vector()

        # mean_vector = self.mean()

        return vector_1 *1, vector_2

    def slope(self):

        return self.y/self.x

    def inv(self):

        return vector(-self.x, -self.y)

    def rotate(self, theta, vector_0):  # rotate x,y around xo,yo by theta (rad)
        xr = math.cos(theta) * (self.x - vector_0.x) - math.sin(theta) * (self.y - vector_0.y) + vector_0.x
        yr = math.sin(theta) * (self.x - vector_0.x) + math.cos(theta) * (self.y - vector_0.y) + vector_0.y
        self.x = int(xr)
        self.y = int(yr)
