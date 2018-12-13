"""
Skill class module
"""
from random import random
from .colors import Colors


class Skill:
    """ special kind of attack that needs EP to be casted """

    # how much damage intelect point adds
    INTELECT_FACTOR = 5

    def __init__(self, name, ep_cost, damage, hit_chance):
        """
        :param name: name of the skill
        :param ep_cost: how much the skill costs to cast
        :param damage: how much damage does the skill deal
        :param hit_chance: probability of hitting the target
        """
        self.name = name
        self.ep_cost = ep_cost
        self.damage = damage
        self.hit_chance = hit_chance

    def recalculate_skill(self, intelect=1):
        """
        recalculates skill damage
        :param intelect: how much is skill damage increased
        """
        self.damage += self.INTELECT_FACTOR + intelect
        self.hit_chance = (self.hit_chance + self.INTELECT_FACTOR * intelect
                           if self.hit_chance + self.INTELECT_FACTOR
                           * intelect < 100
                           else 100)

    def attack(self):
        """
        computes damage done by a skill.
        :param intelect: intelect of a player
        :returns: damage done
        """
        chance = self.hit_chance / 100
        return self.damage if 0 <= random() <= chance else 0

    def __str__(self):
        """ returns skill string with colors """
        name = (Colors.BOLD + self.name + Colors.END).ljust(32)
        damage = (str(self.damage) + " damage").ljust(11)
        ep = (str(self.ep_cost) + " EP cost").ljust(13)
        hit_chance = (str(self.hit_chance) + "% hit chance").ljust(18)
        return name + damage + hit_chance + ep
