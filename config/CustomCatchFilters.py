# TODO add list of available fields to filter on
# TODO add option for a Discord webhook when a custom is caught
from modules.Config import config_general
from modules.Console import console

def CustomCatchFilters(pokemon: dict) -> bool:
    """
    Check the current encounter, catch if it matches any of the following criteria
    Some examples are provided (most are disabled by default)

    `return True` will command the bot to catch the current encounter
    `pass` - will skip the check, and continue to check other criteria further down this file

    Note: you must restart the bot after editing this file for changes to take effect!

    :param pokemon: Pokémon object of the current encounter
    """
    try:
        ivs = [pokemon['IVs']['hp'],
               pokemon['IVs']['attack'],
               pokemon['IVs']['defense'],
               pokemon['IVs']['speed'],
               pokemon['IVs']['spAttack'],
               pokemon['IVs']['spDefense']]

        ### Edit below this line ###

        # Any 1-time encounter Pokémon (starters/legendaries/gift Pokémon) in this exceptions list will not be checked
        exceptions = ['Kyogre', 'Groudon', 'Rayquaza', 'Regirock', 'Regice', 'Registeel', 'Latios', 'Latias', 'Mew',
                      'Lugia', 'Ho-Oh', 'Deoxys', 'Articuno', 'Zapdos', 'Moltres', 'Mewtwo', 'Raikou', 'Entei',
                      'Suicine', 'Castform', 'Lileep', 'Anorith', 'Wynaut', 'Beldum', 'Togepi', 'Eevee', 'Omanyte',
                      'Kabuto', 'Hitmonlee', 'Hitmonchan']

        if pokemon['name'] not in exceptions and config_general['bot_mode'] != 'starters':
            # Catch perfect IV Pokémon
            if pokemon['IVSum'] == 186:
                return True  # ✅ enabled

            # Catch zero IV Pokémon
            if pokemon['IVSum'] == 0:
                return True  # ✅ enabled

            # Catch Pokémon with 6 identical IVs of any value
            if all(v == ivs[0] for v in ivs):
                return True  # ✅ enabled

            # Catch Pokémon with 4 or more max IVs in any stat
            max_ivs = sum(1 for v in ivs if v == 31)
            if max_ivs > 4:
                pass  # ❌ disabled

            # Catch Pokémon with a good IV sum of greater than or equal to 170
            if pokemon['IVSum'] >= 170:
                pass  # ❌ disabled

            # Catch uncaught Pokémon, not yet registered in the dex
            if pokemon['hasSpecies'] == 0:
                pass  # ❌ disabled

            # Catch all Poochyena with a Pecha Berry
            if pokemon['name'] == 'Poochyena' and pokemon['itemName'] == 'Pecha Berry':
                pass  # ❌ disable

            # Catch any Pokémon with perfect attack, spAttack and speed
            if pokemon['IVs']['attack'] == 31 and pokemon['IVs']['spAttack'] == 31 and pokemon['IVs']['speed'] == 31:
                pass  # ❌ disable

        ### Edit above this line ###

        return False
    except:
        console.print_exception(show_locals=True)
        console.print('[red bold]Failed to check Pokemon, potentially due to invalid custom catch filter...')
        return False