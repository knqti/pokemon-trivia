import logging
import requests
import time
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
    sprite_outline_path: str=None
    sprite_reveal_path: str=None
    cry_path: str=None

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

@dataclass
class GameStats:
    start_time: float=time.time()
    questions: int=0
    wrong_guesses: int=0
    correct_answers: int=0
    hints: int=0
    reveals: int=0

    def record_questions(self):
        self.questions += 1

    def record_wrong_guesses(self):
        self.wrong_guesses += 1

    def record_correct_answers(self):
        self.correct_answers += 1

    def record_hints(self):
        self.hints += 1

    def record_reveals(self):
        self.reveals += 1

    def calculate_stats(self):
        if self.questions == 0:
            return 0, 0, 0, 0

        time_played = time.time() - self.start_time
        accuracy = round(self.correct_answers / self.questions * 100)
        hint_rate = round(self.hints / self.questions * 100)
        gave_up_rate = round(self.reveals / self.questions * 100)

        return time_played, accuracy, hint_rate, gave_up_rate
        
    def summary(self):
        time_played, accuracy, hint_rate, gave_up_rate = self.calculate_stats()

        title = 'Game Stats'
        print()
        print('#' * len(title))
        print(title)
        print('#' * len(title))

        print(f'\nPlay Time: {round(time_played / 60, 2)} min.')
        print(f'Total questions: {self.questions}')
        print(f'Correct answers: {self.correct_answers}')
        print(f'Wrong guesses: {self.wrong_guesses}')
        print(f'Hints used: {self.hints}')
        print(f'Revealed answers: {self.reveals}')
        print('-' * len(title))
        print(f'You were correct {accuracy}% of the time.')
        print(f'You needed help {hint_rate}% of the time.')
        print(f'You gave up {gave_up_rate}% of the time.')
