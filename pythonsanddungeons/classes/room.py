"""Module handling Room class"""
import sys
from .middleware import Middleware


class Room:
    """
    Room class with mobs
    """

    def __init__(self, monsters):
        """
        :param monsters: list of monsters in the room
        """
        self.monsters = monsters
        self.dead_monsters = []

    def fight(self, player):
        """
        method handling fight between player and monsters in the room
        :param player: players object
        """
        xp_gain = 0
        while player.hp > 0 and self.look_for_living_monsters():
            player.refill_ep()
            print(player)
            print()

            for monster in self.monsters:
                monster.refill_ep()
            monster_index = 0
            if bool(len(self.monsters) - 1):
                monster_index = self.choose_monster_to_attack()
            else:
                print(self.monsters[0])
            damage = player.attack()
            print()

            if damage > 0:
                xp_gain += self.monsters[monster_index].receive_damage(damage)
                print("You've hit {} dealing {} damage!".format(
                    self.monsters[monster_index].name, damage
                ))
            else:
                print("{} has dodged your attack...".format(
                    self.monsters[monster_index].name
                ))
            self.look_for_living_monsters()
            for monster in self.monsters:
                damage = monster.attack(player.dodge_chance())
                player.receive_damage(damage)
            print()
        if player.hp <= 0:
            print("You have died!")
            sys.exit()
        else:
            print("Well done! You've received {} experience!".format(
                int(xp_gain)
            ))
            player.receive_xp(xp_gain)
            weapon = self.choose_drop(player.stats["Strength"])
            player.heal()
            if weapon:
                player.equipped_weapon = weapon
                player.equipped_weapon.recalculate_weapon(
                    player.stats["Strength"])

    def choose_drop(self, strength):
        """
        asks player to choose which weapon to pick up
        :param strength: how much is weapon better in players hands
        """
        for monster in self.dead_monsters:
            monster.equipped_weapon.recalculate_weapon(strength)
        weapons = [x.equipped_weapon for x in self.dead_monsters]
        prompt1 = ("Do you wish to take one of the dropped weapons?"
                   if len(weapons) - 1
                   else "Do you wish to pick up the weapon?")
        print(prompt1)
        prompt2 = (
            ("Choose 1-{} to pick up weapon or 0 to cancel: ").format(
                len(weapons))
            if len(weapons) - 1 else
            "Press 1 to pick up the weapon or 0 to cancel: "
        )
        range_start, range_end = ((0, len(weapons)) if len(weapons) - 1
                                  else (0, 1))
        print(Middleware.indexed_items(weapons, True))
        weapon_index = Middleware.number(prompt2, range_start, range_end)
        return weapons[weapon_index - 1] if weapon_index else 0

    def choose_monster_to_attack(self):
        """
        asks user to choose a monster to attack
        :returns: index of chosen monster in a list
        """
        self.print_monsters(True)
        prompt = "What monster do you wish to attack? ({}-{}): ".format(
            1, len(self.monsters)
        )
        return Middleware.number(prompt, 1, len(self.monsters)) - 1

    def print_monsters(self, indexing=False):
        """
        pretty prints all the monsters in the room
        :param indexing: indexing of the output
        """
        index = 1
        for monster in self.monsters:
            if indexing:
                print("({}) {}".format(index, monster))
                index += 1
            else:
                print(monster)

    def look_for_living_monsters(self):
        """
        checks if any of the monsters in the room are alive
        :returns: True if any of monsters is alive else False
        """
        for index, monster in enumerate(self.monsters):
            if monster.hp == 0:
                self.dead_monsters.append(self.monsters[index])
                del self.monsters[index]
        return bool(len(self.monsters))
