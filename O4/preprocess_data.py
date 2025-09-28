import json

# Define the name of the file to load
DATA_FILENAME = 'all_pokemon_data.json'
# Define the name for the final, labeled output file
OUTPUT_FILENAME = 'preprocessed_pokemon_data.json'

# A comprehensive list of all legendary and mythical Pokémon
LEGENDARY_POKEMON_NAMES = {
    # Legendaries
    "articuno", "zapdos", "moltres", "mewtwo", "raikou", "entei", "suicune",
    "lugia", "ho-oh", "regirock", "regice", "registeel", "latias", "latios",
    "kyogre", "groudon", "rayquaza", "uxie", "mesprit", "azelf", "dialga",
    "palkia", "heatran", "regigigas", "giratina", "cresselia", "cobalion",
    "terrakion", "virizion", "tornadus", "thundurus", "reshiram", "zekrom",
    "landorus", "kyurem", "xerneas", "yveltal", "zygarde", "tapu-koko",
    "tapu-lele", "tapu-bulu", "tapu-fini", "cosmog", "cosmoem", "solgaleo",
    "lunala", "necrozma", "zacian", "zamazenta", "eternatus", "kubfu",
    "urshifu", "regieleki", "regidrago", "glastrier", "spectrier", "calyrex",
    "enamorus", "wo-chien", "chien-pao", "ting-lu", "chi-yu", "koraidon", "miraidon",
    "ogerpon", "fezandipiti", "munkidori", "okidogi", "pecharunt", "terapagos", 
    "ogerpon-wellspring-mask", "ogerpon-hearthflame-mask", "ogerpon-cornerstone-mask", 
    "terapagos-terastal", "terapagos-stellar", "miraidon-glide-mode", "miraidon-aquatic-mode",
    "miraidon-drive-mode", "miraidon-low-power-mode", "koraidon-gliding-build", "koraidon-swimming-build",
    "koraidon-sprinting-build", "koraidon-limited-build", "palkia-origin", "dialga-origin",
    "urshifu-rapid-strike", "eternatus-eternamax", "zamazenta-crowned", "zacian-crowned",
    "zygarde-10", "moltres-galar", "zapdos-galar", "articuno-galar", "necrozma-ultra", 
    "necrozma-dawn", "necrozma-dusk", "giratina-origin",  "zygarde-complete",
    "zygarde-50-power-construct", "zygarde-10-power-construct", "hoopa-unbound",
    "rayquaza-mega", "groudon-primal", "kyogre-primal", "mewtwo-mega-x", "mewtwo-mega-y",
    "latias-mega", "latios-mega", "kyurem-white", "kyurem-black", "giratina-altered",
    "cresselia-lunar", "landorus-therian", "thundurus-therian", "tornadus-therian",
    "deoxys-attack", "deoxys-defense", "deoxys-speed", "deoxys-normal",

    # Mythicals
    "mew", "celebi", "jirachi", "deoxys", "phione", "manaphy", "darkrai",
    "shaymin", "arceus", "victini", "keldeo", "meloetta", "genesect",
    "diancie", "hoopa", "volcanion", "magearna", "marshadow", "zeraora",
    "meltan", "melmetal", "zarude", "magearna-original", "shaymin-sky"
}

def process_and_label_data():
    """
    Loads raw Pokémon data, extracts key features, adds a legendary label,
    and saves the final processed data to a new JSON file.
    """
    try:
        # 1. Load the raw JSON file
        print(f"Loading raw data from '{DATA_FILENAME}'...")
        with open(DATA_FILENAME, 'r', encoding='utf-8') as f:
            all_pokemon_data = json.load(f)
        
        print(f"Successfully loaded data for {len(all_pokemon_data)} Pokémon.")
        print("-" * 30)

        # 2. Process and label the data
        final_labeled_list = []
        legendary_count = 0
        print("Preprocessing and labeling all Pokémon...")

        for pokemon in all_pokemon_data:
            stats = {stat['stat']['name']: stat['base_stat'] for stat in pokemon['stats']}
            name = pokemon['name']

            # Create a new dictionary containing the desired data
            processed_pokemon = {
                'id': pokemon['id'],
                'name': name,
                'height': pokemon.get('height'),
                'weight': pokemon.get('weight'),
                'hp': stats.get("hp"),
                'attack': stats.get("attack"),
                'defense': stats.get("defense"),
                'special-attack': stats.get("special-attack"),
                'special-defense': stats.get("special-defense"),
                'speed': stats.get("speed"),
                'moves_count': len(pokemon.get('moves', [])),
                'base_experience': pokemon.get('base_experience'),
                'held_items_count': len(pokemon.get('held_items', [])),
                'type_1': pokemon['types'][0]['type']['name'] if len(pokemon['types']) > 0 else 0,
                'type_2': pokemon['types'][1]['type']['name'] if len(pokemon['types']) > 1 else 0,
            }

            # Add the legendary label
            if name in LEGENDARY_POKEMON_NAMES:
                processed_pokemon['is_legendary'] = 1
                legendary_count += 1
            else:
                processed_pokemon['is_legendary'] = 0
            
            final_labeled_list.append(processed_pokemon)
            
        print(f"Successfully processed and labeled {len(final_labeled_list)} Pokémon.")
        print(f"Found {legendary_count} legendary/mythical Pokémon.")

        # 3. Save the final labeled list to a file
        print(f"Saving final labeled data to '{OUTPUT_FILENAME}'...")
        with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f:
            json.dump(final_labeled_list, f, ensure_ascii=False, indent=4)
        
        print(f"✅ All done! Labeled data saved to '{OUTPUT_FILENAME}'.")

    except FileNotFoundError:
        print(f"Error: The file '{DATA_FILENAME}' was not found.")
        print("Please make sure you have run the 'fetch_pokemon_data.py' script first.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    process_and_label_data()
