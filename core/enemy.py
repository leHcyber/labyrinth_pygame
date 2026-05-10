from enum import Enum

class EnemyType(Enum):
    MONSTRE = "M"
    MONSTRE2 = "M2"
    MONSTRE3 = "M3"
    MONSTRE4 = "M4"
    MONSTRE5 = "M5"
    MONSTRE6 = "M6"
    BOSS = "X"
    BOSS2 = "X2"
    BOSS3 = "X3"

class EnemyTest:
    def __init__(self, type: EnemyType, health, attack):
        self.type = type
        self.health = health
        self.attack = attack

class Enemy:
    def __init__(self, name, hp, attack, enemy_type):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.type = enemy_type

    def take_damage(self, dmg):
        self.hp = max(0, self.hp - dmg)

    def is_dead(self):
        return self.hp <= 0

    def get_damage(self):
        return self.attack


class EnemyFactory:
    DATA = {
        "M": ("Monstre", 7, 2),
        "M2": ("Monstre 2", 4, 1),
        "M3": ("Monstre 3", 5, 1),
        "M4": ("Monstre 4", 4, 2),
        "M5": ("Monstre 5", 6, 1),
        "M6": ("Monstre 6", 7, 2),
        "X": ("Boss", 9, 2),
        "X2": ("Boss 2", 8, 2),
        "X3": ("Boss 3", 13, 2),
    }

    @staticmethod
    def create(enemy_type):
        name, hp, atk = EnemyFactory.DATA[enemy_type]
        return Enemy(name, hp, atk, enemy_type)