import json
import logging
from pprint import pprint
from src.classes import ApiClient, Pokemon
from src.paths import PATHS

logger = logging.getLogger(__name__)

def catch_pokemon(pokemon_id: int, api_client: object=ApiClient()):
    
    def call_pokemon_endpoints(i: int) -> dict:
        pokemon = api_client.get_pokemon(id=i)
        flavor_text = api_client.get_flavor_text(id=i)

        # Combine data into dictionary
        pokemon_dict = {
            'id': pokemon.id,
            'name': pokemon.name,
            'types': pokemon.types,
            'height': pokemon.height,
            'weight': pokemon.weight,
            'abilities': pokemon.abilities,
            'held_items': pokemon.held_items,
            'sprites': pokemon.sprites,
            'cries': pokemon.cries,
            'flavor_text': flavor_text.flavor_text
        }
        return pokemon_dict

    data = call_pokemon_endpoints(pokemon_id)
    
    output_path = PATHS['pokemon'] / f'pokemon_id_{pokemon_id}.json'
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)   

    logger.info(f'Gotcha! {data['name']} was caught')

def read_pokedex(pokemon_id: int, to_print: bool=True):
    file_path = PATHS['pokemon'] / f'pokemon_id_{pokemon_id}.json'
    
    with open(file_path, 'r') as f:
        results = json.load(f)

    pokemon = Pokemon(**results)

    if to_print:
        print('Initializing Pokedex...')
        pprint(pokemon)

    return pokemon
