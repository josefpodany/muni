"""
File handling weapon class
"""
from .colors import Colors


class Weapon:
    """ Weapon class """
    RARITY_COLORS = {
        "Common": Colors.GRAY,
        "Uncommon": Colors.GREEN,
        "Rare": Colors.BRIGHT_YELLOW,
        "Epic": Colors.BRIGHT_MAGENTA,
        "Legendary": Colors.BRIGHT_RED
    }
    RARITIES = ["Common", "Uncommon", "Rare", "Epic", "Legendary"]
    STRENGTH_FACTOR = 3

    def __init__(
            self, name, damage, rarity, durability, hit_chance
    ):
        """
        :param name: weapon name
        :param damage: how much damage the weapon deals
        :param rarity: 'common'/'uncommon'/'rare'/'epic'/'legendary'
        :param durability: how much can the weapon be used
        :param hit_chance: chance of hitting the target between 0 and 100
        """
        self.name = name
        self.damage = damage
        self.rarity = rarity
        self.durability = durability
        self.max_durability = durability
        self.hit_chance = hit_chance
        self.broken = False

    def hit(self):
        """
        computes damage done by weapon
        :param strength: players strength
        :returns: damage done
        """
        self.durability = self.durability - 1 if self.durability > 0 else 0
        if self.durability == 0 and not self.broken:
            self.broken = True
            self.damage = self.damage / 2
        return self.damage

    def recalculate_weapon(self, strength=1):
        """
        recalculates weapon damage based on strength
        :param strength: strength of weapon's holder
        """
        broken = 2 if self.broken else 1
        self.damage += int(
            (self.STRENGTH_FACTOR * strength) / broken)

    def __str__(self):
        """ returns weapon string with colors """
        name = (Colors.BOLD + self.name + Colors.END).ljust(32)
        damage = (str(self.damage) + " damage").ljust(11)
        hit_chance = (str(self.hit_chance) + "% hit chance").ljust(18)
        rarity = self.RARITY_COLORS[self.rarity] + self.rarity + Colors.END
        durability = (str(int(self.durability / self.max_durability * 100))
                      + "% durability").ljust(18)
        return name + damage + hit_chance + durability + rarity
