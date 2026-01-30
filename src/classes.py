import logging
import requests
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class Pokemon:
    id: int=None
    name: str=None
    types: list=None
    height: int=None
    weight: int=None
    abilities: list=None
    held_items: list=None
    sprites: str=None
    cries: str=None
    flavor_text: str=None

class ApiClient:

    def get_pokemon(self, id: int, url: str='https://pokeapi.co/api/v2/pokemon') -> Pokemon:
        api_url = f'{url}/{id}'
        response = requests.get(api_url)
        
        try:
            response.raise_for_status()
            data = response.json()

            logger.info(f'A wild Pokemon appeared: ID {id}')

            return Pokemon(
                id=data['id'],
                name=data['name'],
                types=[t['type']['name'] for t in data['types']],
                height=data['height'],
                weight=data['weight'],
                abilities=[a['ability']['name'] for a in data['abilities']],
                held_items=[item['item']['name'] for item in data['held_items']],
                sprites=data['sprites']['front_default'],
                cries=data['cries']['latest']
            )
        except requests.HTTPError as e:
            logger.error(f'Failed to get Pokemon ID {id}: {e}')
            raise

    def get_flavor_text(self, id: int, url: str='https://pokeapi.co/api/v2/pokemon-species') -> Pokemon:
        api_url = f'{url}/{id}'
        response = requests.get(api_url)

        try:
            response.raise_for_status()
            data = response.json()

            logger.info(f'Registering {id}...')

            # Filter for English entries
            english_entries = [entry for entry in data['flavor_text_entries'] if entry.get('language', {}).get('name') == 'en']

            return Pokemon(
                flavor_text = english_entries[0]['flavor_text'] if english_entries else None            
            )
        except requests.HTTPError as e:
            logger.error(f'Failed to get Pokemon ID {id}: {e}')
            raise
