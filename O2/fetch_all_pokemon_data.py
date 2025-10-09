import requests
import json
import os
import time

# Define the name for the output file
OUTPUT_FILENAME = 'all_pokemon_data.json'
# The API endpoint to get the list of all Pokémon.
# We set a high limit to ensure we get all of them in one request.
POKEMON_LIST_URL = 'https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0'

def fetch_all_pokemon_data():
    """
    Fetches detailed data for every Pokémon from the PokéAPI and saves it to a single JSON file.
    """
    print("Starting the Pokémon data fetching process...")

    # Check if the data file already exists to avoid re-downloading.
    if os.path.exists(OUTPUT_FILENAME):
        print(f"'{OUTPUT_FILENAME}' already exists. Skipping download.")
        print("To re-download, please delete the existing file.")
        return

    try:
        # 1. Get the list of all Pokémon resources (name and URL)
        print(f"Fetching the full list of Pokémon from {POKEMON_LIST_URL}...")
        response = requests.get(POKEMON_LIST_URL)
        response.raise_for_status()  # Raise an error for bad status codes
        all_pokemon_list = response.json()['results']
        total_pokemon = len(all_pokemon_list)
        print(f"Found {total_pokemon} Pokémon to fetch.")
        
        all_pokemon_details = []

        # 2. Loop through each Pokémon and fetch its detailed data
        for i, pokemon_summary in enumerate(all_pokemon_list):
            name = pokemon_summary['name']
            url = pokemon_summary['url']
            
            # Print progress to the console
            print(f"Fetching data for {name.title()} ({i + 1}/{total_pokemon})...")
            
            try:
                # Make the request for this specific Pokémon's details
                pokemon_response = requests.get(url)
                pokemon_response.raise_for_status()
                
                # Append the detailed JSON data to our list
                all_pokemon_details.append(pokemon_response.json())
                
                # Be polite to the API by waiting a moment between requests
                time.sleep(0.05)

            except requests.exceptions.RequestException as e:
                print(f"Could not fetch data for {name}. Error: {e}. Skipping...")

        # 3. Save the complete list of data to a file
        print(f"\nAll Pokémon data has been fetched. Saving to '{OUTPUT_FILENAME}'...")
        with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f:
            json.dump(all_pokemon_details, f, ensure_ascii=False, indent=4)
        
        print("✅ Process complete!")
        print(f"All data has been successfully saved to '{OUTPUT_FILENAME}'.")

    except requests.exceptions.RequestException as e:
        print(f"A critical error occurred while fetching the Pokémon list: {e}")
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting.")


if __name__ == '__main__':
    fetch_all_pokemon_data()
