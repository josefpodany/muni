"""Module handling Monster, RareMonster and Boss classes."""
from random import choice
from .character import Character


class Monster(Character):
    """
    Basic monster NPC class
    Inherits melee_attack() and print_skills() methods from Character class.
    """

    def __init__(
            self, name, hp, ep, skills, equipped_weapon,
            xp_gain
    ):
        """
        :param name: players name
        :param hp: health points
        :param ep: energy points
        :param skills: list of monsters skills
        :param equipped_weapon: players equipped weapon
        :param xp_gain: amount of xp the monster drops
        """
        super().__init__(name, skills, equipped_weapon, hp, ep)
        self.xp_gain = xp_gain

    def attack(self, dodge_chance):
        """
        randomly chooses monsters attack based on attack possibilities
        :param dodge_chance: players chance to dodge the attack
        :returns: damage dealt to the player
        """
        available_skills = self.get_available_skills()
        possibilities = ["melee", "skill"] if available_skills else ["melee"]
        attack = choice(possibilities)
        damage = 0
        kind_of_attack = ""
        if attack == "skill":
            skill_index = choice([i for i, _ in enumerate(available_skills)])
            self.ep -= self.skills[skill_index].ep_cost
            damage = self.skills[skill_index].attack()
            kind_of_attack = self.skills[skill_index].name
        else:
            damage = self.melee_attack(dodge_chance)
            kind_of_attack = self.equipped_weapon.name

        if damage == 0:
            print("{} tried to hit you with a {} but missed!".format(
                self.name, kind_of_attack
            ))
        else:
            print("{} hit you with a {} dealing {} damage!".format(
                self.name, kind_of_attack, damage
            ))
        return damage

    def get_available_skills(self):
        """
        finds indices of available skills regarding to ep cost
        :returns: indices of available skills
        """
        available_skills = []
        for skill_index, skill in enumerate(self.skills):
            if skill.ep_cost <= self.ep:
                available_skills.append(skill_index)
        return available_skills

    def receive_damage(self, damage):
        """
        handles receiving damage. Returns xp if dead, else 0.
        :param damage: damage done to the monster
        :returns: 0 if not dead else amount of xp
        """
        if self.hp - damage <= 0:
            self.hp = 0
            return self.xp_gain
        self.hp -= damage
        return 0
