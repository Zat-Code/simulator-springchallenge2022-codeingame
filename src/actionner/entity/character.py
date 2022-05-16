from src.utils.vector import vector


class Character:

    def __init__(self, x, y, id, type_character, shield_life, is_controlled, health, vx, vy, near_base, threat_for, velocity):

        self.id = id
        self.type = type_character

        self.shield_life = shield_life
        self.is_controlled = is_controlled
        self.health = health
        self.trajectory = vector(vx, vy)
        self.near_base = near_base
        self.threat_for = threat_for

        self.vx = vx
        self.vy = vy

        self.position = vector(x, y)
        self.velocity = velocity
