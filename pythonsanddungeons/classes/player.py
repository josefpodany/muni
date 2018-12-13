""" Player module """
from .middleware import Middleware
from .character import Character
from .colors import Colors


class Player(Character):
    """
    Player class
    Inherits melee_attack() and print_skills() methods from Character class.
    """

    def __init__(self, name, skills, equipped_weapon, hp=100, ep=100):
        """
        :param name: players name
        :param skills: array of players skills
        :param equipped_weapon: players equipped weapon
        :param hp: health points
        :param ep: energy points
        """
        super().__init__(name, skills, equipped_weapon, hp, ep)
        self.level = 1
        self.xp = 0
        self.next_level = 100
        self.stats = {
            "Vitality": 0,
            "Strength": 0,
            "Agility": 0,
            "Intelect": 0
        }

    def receive_xp(self, xp):
        """
        adds xp to player
        :param xp: number of xp received from monsters
        """
        if self.xp + xp >= self.next_level:
            self.xp = self.xp + xp - self.next_level
            self.level += 1
            self.next_level = int(self.next_level * 1.2)
            print(self.get_stats(True))
            self.increase_stat()
            self.hp = self.max_hp
            self.ep = self.max_ep
        else:
            self.xp += xp

    def receive_damage(self, damage):
        """
        subtracts damage from player's health
        :param damage: amount of damage received
        """
        self.hp -= damage

    def attack(self):
        """
        asks user what attack to use and evaluates that attack
        :returns: damage dealt by melee attack or skill
        """
        prompt = "Choose what attack to use from 1 to {}: ".format(
            len(self.skills) + 1)
        while True:
            choice = Middleware.number(prompt, 1, len(self.skills) + 1)
            if choice == 1:
                return self.melee_attack(self.hit_chance())
            else:
                if self.skills[choice - 2].ep_cost <= self.ep:
                    self.ep -= self.skills[choice - 2].ep_cost
                    return self.skills[choice - 2].attack()
                else:
                    print("Insufficient ep to cast that skill!")

    def heal(self, amount=20):
        """
        heals player for certain amount
        :param amount: how much hp is added
        """
        self.hp = (self.max_hp
                   if self.hp + amount > self.max_hp
                   else self.hp + amount)

    def hit_chance(self):
        """
        computes hit chance according to agility from 0 to
        :returns: hit chance
        """
        return self.stats["Agility"] * 0.04

    def dodge_chance(self):
        """
        computes chance to dodge the attack from 0 to 1
        :returns: dodge chance
        """
        return self.stats["Agility"] * 0.05

    def increase_stat(self):
        """
        increases user's stats and reevaluates skills and weapon damage
        :param index: index of stat to increase by 1
        """
        output = "Choose between 1 and {} to increase your stats: ".format(
            len(self.stats))
        index = Middleware.number(output, 1, len(self.stats))
        stat = list(self.stats.keys())[index - 1]
        self.stats[stat] += 1
        if stat == "Vitality":
            self.max_hp += 20
            self.hp += 20
        elif stat == "Strength":
            self.equipped_weapon.recalculate_weapon()
        elif stat == "Intelect":
            self.max_ep += 10
            self.ep += 10
            for skill in self.skills:
                skill.recalculate_skill()

    def get_stats(self, indexing=False):
        """
        prints statistics of players atributes.
        :param indexing: indexes the output of atributes
        :returns: statistics
        """
        items = ["{}: {}".format(key, item)
                 for (key, item) in self.stats.items()]
        return Middleware.indexed_items(items, indexing)

    def __str__(self):
        """ prints complete info about player"""
        level = "Lvl. " + str(self.level) + " "
        name = (Colors.BOLD + self.name + Colors.END).ljust(40)
        hp = (Colors.BRIGHT_RED + str(self.hp) + "\\" +
              str(self.max_hp) + "HP" + Colors.END).ljust(22)
        ep = (Colors.BRIGHT_MAGENTA + str(self.ep) + "\\" +
              str(self.max_ep) + "EP" + Colors.END).ljust(22)
        xp = (str(self.xp) + "\\" + str(self.next_level) + "XP")
        weapon = "({}) {}".format(1, self.equipped_weapon)
        return "-" * 85 + "\n" + level + name + hp + ep + xp + "\n" + \
            weapon + "\n" + self.get_skills(indexing=True, start=2) \
            + "\n" + "-" * 85
