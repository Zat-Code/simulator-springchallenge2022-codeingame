



class ParseObjectToList:

    def __init__(self, player_1, player_2, monsters):

        self.player_1 = player_1
        self.player_2 = player_2

        self.monsters = monsters


    def parse_for_player_1(self):

        player_1 = (self.player_1.life, self.player_1.mana)
        player_2 = (self.player_2.life, self.player_2.mana)

        entity = []
        for i, hero in enumerate(self.player_1.heroes.heroes):
            entity.append((hero.id, hero.type, hero.position.x, hero.position.y, hero.shield_life, hero.is_controlled,
                           hero.health, hero.vx, hero.vy, hero.near_base, hero.threat_for))

        for hero in self.player_2.heroes.heroes:
            entity.append((hero.id, hero.type, hero.position.x, hero.position.y, hero.shield_life, hero.is_controlled,
                           hero.health, hero.vx, hero.vy, hero.near_base, hero.threat_for))

        for monster in self.monsters.monsters:
            if monster.see_per_base_player_1 == 1 or monster.see_per_heroes_player_1 > 0:
                entity.append((monster.id, monster.type, monster.position.x, monster.position.y, monster.shield_life,
                               monster.is_controlled, monster.health, monster.vx, monster.vy, monster.near_base,
                               monster.threat_for))

        return player_1, player_2, len(entity), entity

    def parse_for_player_2(self):

        conversion= {2: 1,
                     1: 2,
                     0: 0,
                     -1: -1,
                     }

        player_1 = (self.player_1.life, self.player_1.mana)
        player_2 = (self.player_2.life, self.player_2.mana)

        entity = []
        for hero in self.player_1.heroes.heroes:
            entity.append((hero.id+3, conversion[hero.type], hero.position.x, hero.position.y, hero.shield_life, hero.is_controlled,
                           hero.health, hero.vx, hero.vy, conversion[hero.near_base], conversion[hero.threat_for]))

        for i, hero in enumerate(self.player_2.heroes.heroes):
            entity.append((hero.id-3, conversion[hero.type], hero.position.x, hero.position.y, hero.shield_life, hero.is_controlled,
                           hero.health, hero.vx, hero.vy, conversion[hero.near_base], conversion[hero.threat_for]))

        for monster in self.monsters.monsters:
            if monster.see_per_base_player_2 == 1 or monster.see_per_heroes_player_2 > 0:
                entity.append((monster.id, conversion[monster.type], monster.position.x, monster.position.y, monster.shield_life,
                               monster.is_controlled, monster.health, monster.vx, monster.vy, conversion[monster.near_base],
                               conversion[monster.threat_for]))

        return player_1, player_2, len(entity), entity
