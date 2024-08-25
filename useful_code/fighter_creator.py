import pygame
import sys

class Fighter:
    """
    A class for making a fighter.
    """
    def __init__(self, name: str, x: int, y: int, equipment: list, health: int, max_health: int, base_attack: int, base_defence: int, level: int, effects: list):
        """
        Initialises all variables for the fighter.
        :param name: Name of the fighter
        :param x: X coordinate of the fighter
        :param y: Y coordinate of the fighter
        :param equipment: The fighter's equipped items
        :param health: Current health of the fighter
        :param max_health: Maximum health of the fighte
        :param base_attack: Base attack damage of the fighter
        :param base_defence: Base defence value of the fighter
        :param level: Current level of the fighter (max level 50)
        :param effects: A list of all effects the fighter has (e.g. weak)
        """
        self.name = name
        self.x = x
        self.y = y
        self.equipment = equipment
        self.health = health
        self.max_health = max_health
        self.base_attack = base_attack
        self.base_defence = base_defence
        self.attack = self.base_attack
        self.defence = self.base_defence
        self.level = level
        self.effects = effects

    def level_up(self):
        """
        Levels up the fighter and increases their stats.
        """
        self.level += 1
        self.base_attack += 1
        self.max_health += 5
        if self.level % 5 == 0:
            self.base_defence += 1
            self.defence += 1
        self.attack = self.base_attack
