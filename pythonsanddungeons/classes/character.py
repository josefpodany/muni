"""
Character, Player, Monster, Rare Monster, Boss classes Module
"""
from random import random
from .colors import Colors
from .middleware import Middleware


class Character:
    """ Character class """

    def __init__(self, name, skills, equipped_weapon, hp=100, ep=100):
        """
        highest class representing single game character
        :param name: characters name
        :param hp: health points
        :param ep: energy points
        :param skills: list of skills
        :param equipped_weapon: characters weapon
        """
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.ep = ep
        self.max_ep = ep
        self.skills = skills
        self.equipped_weapon = equipped_weapon

    def melee_attack(self, hit_chance=0, dodge_chance=0):
        """
        calculates melee attack
        :param dodge_chance: defenders chance to parry the hit
        :param hit_chance: attackers ability to hit the target
        :returns: returns damage dealt, half if the weapon is broken
        """
        chance = (self.equipped_weapon.hit_chance / 100 +
                  hit_chance - dodge_chance)
        if 0 <= random() <= chance:
            return self.equipped_weapon.hit()
        return 0

    def get_skills(self, indexing=False, start=1):
        """
        prints all the available skills and their info.
        :param indexing: indexes the output of skills
        :param start: starting index of output
        :returns: string of all skills
        """
        return Middleware.indexed_items([skill for skill in self.skills],
                                        indexing, start)

    def refill_ep(self, amount=10):
        """
        refills ep to the character
        :param amount: how much ep will be added
        """
        self.ep = (self.max_ep
                   if self.ep + amount > self.max_ep
                   else self.ep + amount)

    def __str__(self):
        """ overloads print function and adds colors """
        name = (Colors.BOLD + self.name + Colors.END).ljust(40, " ")
        hp = (str(self.hp) + "\\" + str(self.max_hp) + "HP").ljust(12, " ")
        ep = (str(self.ep) + "\\" + str(self.max_ep) + "EP").ljust(12, " ")
        weapon = "\n\t" + str(self.equipped_weapon)
        skills_string = "\n"
        for skill in self.skills:
            skills_string += "\t" + str(skill) + "\n"
        return (name + hp + ep + weapon + skills_string).rstrip()
