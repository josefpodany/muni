""" Main game module """
from classes import Gameplan, Middleware, Player
"""
Autor: Josef Podaný, 485460

Prohlašuji, že celý zdrojový kód jsem zpracoval(a) zcela samostatně. Jsem si
vědom(a), že  nepravdivost tohoto tvrzení může být důvodem k hodnocení F v
předmětu IB111 a k disciplinárnímu řízení.

Známé nedostatky: Na žádné jsem nenarazil, ale v takhle obsáhlém kódu se jich
určitě dost najde.

Styl: Nelíbí se mi printování všude možně. Ideální by byla třída řešící GUI,
kde by byla možnost printovat do terminálu a výstup přepisovat místo
vypisování pod sebe.
Některé třídy mají podle linteru příliš mnoho atributů a parametrů
v konstruktorech.
Názvy proměnných jsou někdy krátké (xp, hp, ep).
"""

if __name__ == '__main__':
    PROMPT1 = "What theme do you wish to play? Fantasy (f) or School (s) themed?: "
    PROMPT2 = "Choose easy (e), medium (m) or hard (h) difficulty: "
    REGEX1 = "^[fs]$"
    REGEX2 = "^[emh]$"
    PLAYER_NAME = Middleware.string("Choose your name: ")
    THEME = Middleware.string(PROMPT1, REGEX1)
    DIFFICULTY = Middleware.string(PROMPT2, REGEX2)
    GAMEPLAN = Gameplan(THEME, DIFFICULTY)
    GAMEPLAN.set_up_rooms()
    PLAYER = Player(PLAYER_NAME, GAMEPLAN.get_skills(amount=2),
                    GAMEPLAN.get_weapon(rarity="Uncommon"))
    # redisribute the first 4 atribute points
    print("Where do you wish to redistribute your first 5 atribute points? ")
    print(PLAYER.get_stats(True))
    for _ in range(5):
        PLAYER.increase_stat()
    print(PLAYER.get_stats(True))
    GAMEPLAN.play(PLAYER)
