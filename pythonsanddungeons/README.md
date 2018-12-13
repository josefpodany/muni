# Dungeons and Pythons

## Requirements

-   python3.6 and higher

-   preferably dark terminal theme for optimal readability

## How to play

1. run \_\_main\_\_.py

2. select one of three difficulties:
    - easy - 4 rooms, 1 monster in each room
    - medium - 6 rooms, 1 - 2 monsters in each room
    - hard - 8 rooms, 2 - 3 monsters in each room
3. select theme - school or fantasy (more RPG-like)
4. redistribute your first 5 atribute points
5. enjoy the game!

## Rules

-   player and each monster have one attack per turn

-   10HP and 20EP is regenerated after every beaten room

-   you can add another atribute point during every next level-up

-   player wins if all rooms are beaten

## Atributes

-   strength - melee attack does more damage

-   agility - higher hit chance of melee attack and dodge chance

-   vitality - every point adds another 10 points to maximum health

-   intelect - skills do more damage and have higher chance to hit the target

## Adding custom monsters, weapons and skills formats

-   monsters.csv - name;theme('f'/'s'),type('mob'/'boss')

-   skills.csv - name;ep_cost;damage;hit_chance;theme('f'/'s');type('anyone'/'boss')

-   weapons.csv - name;theme('f'/'s');type('anyone'/'boss');damage;rarity('Common'/'Uncommon'/'Rare'/'Epic'/'Legendary');durability;hit_chance
    -   warning - bosses assign only weapons with rarity of Legendary
