from src.utils.vector import vector


class Config:

    def __init__(self):

        self.MAP_WIDTH = 17630
        self.MAP_HEIGHT = 9000
        self.MAP_LIMIT = 800

        self.MAX_TURN = 220

        self.BASE_ATTRACTION_RADIUS = 5000
        self.BASE_VIEW_RADIUS = 6000
        self.BASE_RADIUS = 300

        self.MAX_MAX = -1
        self.STARTING_MANA = 0
        self.STARTING_BASE_LIFE = 3

        self.HERO_MOVE_SPEED = 800
        self.HEROES_PER_PLAYER = 3
        self.HERO_VIEW_RADIUS = 2200
        self.HEROES_ATTACK_RANGE = 800
        self.HERO_ATTACK_DAMAGE = 2

        self.POSITION_START_HEROES_PLAYER_1 = [vector(1131, 1131), vector(1414, 849), vector(849, 1414)]
        self.POSITION_START_HEROES_PLAYER_2 = [vector(16499, 7869), vector(16216, 8151), vector(16781, 7586)]

        self.MOB_MOVE_SPEED = 400
        self.SPAWN_RANGE = 4000

        self.SPELL_WIND_COST = 10
        self.SPELL_CONTROL_COST = 10
        self.SPELL_PROTECT_COST = 10
        self.SPELL_PROTECT_DURATION = 12
        self.SPELL_WIND_DISTANCE = 2200
        self.SPELL_WIND_RADIUS = 1280
        self.SPELL_CONTROL_DISTANCE = 2200
        self.SPELL_SHIELD_DISTANCE = 2200


