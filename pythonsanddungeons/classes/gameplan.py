""" Gameplan module """
import sys
from collections import deque
from random import randint, choice, sample
from .middleware import Middleware
from .monster import Monster
from .skill import Skill
from .weapon import Weapon
from .room import Room
from .colors import Colors


class Gameplan:
    """ Complete Gameplan class for Dungeons&Pythons """
    DIFFICULTIES = {
        "e": {
            "rooms": 4,
            "monsters": (1, 1),
            "factor": 1
        },
        "m": {
            "rooms": 6,
            "monsters": (1, 2),
            "factor": 1.1
        },
        "h": {
            "rooms": 8,
            "monsters": (2, 3),
            "factor": 1.2
        }
    }
    MONSTERS_PATH = "./static/monsters.csv"
    WEAPONS_PATH = "./static/weapons.csv"
    SKILLS_PATH = "./static/skills.csv"

    def __init__(self, theme, difficulty):
        """
        :param theme: 's'/'f' for school/fantasy
        :param difficulty: 'e'/'m'/'h' for easy/medium/hard
        """
        self.rooms = deque()
        self.theme = theme
        self.difficulty = difficulty
        self.weapons = [weapon for weapon in self.load_weapons()
                        if theme in weapon]
        self.skills = [skill for skill in self.load_skills() if theme in skill]

    def play(self, player):
        """
        main method for playing the game
        :param player: player object
        """
        for index, room in enumerate(self.rooms):
            print("-" * 39 + Colors.BOLD + " ROOM " +
                  str(index + 1) + " " + Colors.END + "-" * 38)
            room.fight(player)

    def set_up_rooms(self):
        """
        generates rooms in regards to difficulty and theme
        """
        mobs = [mob for mob in self.load_monsters() if self.theme in mob]
        generic_mobs = [mob for mob in mobs if "mob" in mob]
        bosses = [boss for boss in mobs if "boss" in boss]
        # number of monsters in a room
        range_start, range_end = self.DIFFICULTIES[self.difficulty]["monsters"]
        for i in range(self.DIFFICULTIES[self.difficulty]["rooms"]):
            monsters = []
            number_of_mobs = choice([range_end, range_start])
            if i == self.DIFFICULTIES[self.difficulty]["rooms"] - 1:
                # add boss to the last room
                number_of_mobs -= 1
                skills = self.get_skills(assign="boss") + self.get_skills()
                monsters.append(
                    self.create_monster(
                        choice(bosses),
                        skills,
                        self.get_weapon(assign="boss", rarity="Legendary"),
                        200, 150, 300))

            if number_of_mobs >= range_start:
                # create normal room depending on the max amount of monsters
                # in the room
                weapons_end_range = 3 if i > 3 else i
                for _ in range(randint(range_start, number_of_mobs)):
                    rarity = choice(Weapon.RARITIES[:weapons_end_range + 1])
                    monsters.append(self.create_monster(choice(generic_mobs),
                                                        self.get_skills(),
                                                        self.get_weapon(
                                                            assign="anyone",
                                                            rarity=rarity),
                                                        50, 50, 50))
            self.rooms.append(Room(monsters))

    def create_monster(self, monster, skills, weapon, base_health,
                       base_energy, base_xp_gain):
        """
        creates monster and randomly chooses skill and weapon by monster
        :param monster: monster's name
        :param skills: list of skill objects
        :param weapon: weapon object
        :param base_health: amount of health regardless on difficulty factor
        :param base_energy: amount of energy regardless on difficulty factor
        :param base_xp_gain: amount of xp gain regardless on difficulty factor
        :returns: complete Monster object
        """
        health = int(base_health *
                     self.DIFFICULTIES[self.difficulty]["factor"])
        energy = int(base_energy *
                     self.DIFFICULTIES[self.difficulty]["factor"])
        xp_gain = int(base_xp_gain *
                      self.DIFFICULTIES[self.difficulty]["factor"])
        return Monster(monster[0], health, energy, skills, weapon, xp_gain)

    def load_monsters(self):
        """
        loads data for monster objects
        :returns: 2d list of items for monster objects
        """
        return Middleware.load_csv(self.MONSTERS_PATH)

    def load_weapons(self):
        """
        loads data for weapon objects
        :returns: 2d list of items for weapon objects
        """
        return Middleware.load_csv(self.WEAPONS_PATH)

    def load_skills(self):
        """
        loads data for skill objects
        :returns: 2d list of items for skill objects
        """
        return Middleware.load_csv(self.SKILLS_PATH)

    def get_weapon(self, rarity="anyone", assign="anyone"):
        """
        selects random weapon with rarity
        :param rarity: rarity of weapon
        :param assign: 'anyone'/'boss' who is this weapon for
        :returns: Weapon
        """
        weapon = choice([x for x in self.weapons
                         if rarity in x and assign in x])
        return Weapon(weapon[0], int(weapon[3]), weapon[4],
                      int(weapon[5]), int(weapon[6]))

    def get_skills(self, amount=1, assign="anyone"):
        """
        selects 2 random skills for player
        :param amount: number of generated skills
        :param assign: 'anyone'/'boss' who is this skill for
        :returns: list of skills
        """
        skills_obj = []
        skills = [skill for skill in self.skills if assign in skill]
        if len(skills) < amount:
            print(
                "Too few skills! Go into ./static/skills.csv and add some for anyone to use!")
            sys.exit()
        skill_indeces = sample(range(0, len(skills)), amount)
        for i in skill_indeces:
            skills_obj.append(Skill(skills[i][0], int(skills[i][1]),
                                    int(skills[i][2]), int(skills[i][3])))
        return skills_obj
