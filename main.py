import config
import random
from src.paths import PATHS
from src.tall_grass import read_pokedex
from src.utils import setup
from time import sleep


def ask_question(pokemon: object):
    height_ft = round(pokemon.height * 0.328084, 1)
    weight_lb = round(pokemon.weight * 0.2204623, 1)
    ability = random.choice(pokemon.abilities)

    title = "Who's that POK\u00e9MON?"
    print('#' * len(title))
    print(title)
    print('#' * len(title))

    print(f'\n- This POK\u00e9MON is approxiamately {height_ft} ft. tall and weighs about {weight_lb} lb.\n- It is known to have the ability {ability}.\n')
    print(pokemon.flavor_text)

def check_answer(user_answer: str, correct_answer: str) -> bool:
    user_answer = user_answer

    if user_answer == correct_answer or user_answer == 'help':
        return True
    
    print('Nope try again.')
    return False

def main_loop():
    while True:
        id = random.randint(1, 151)
        mystery_pokemon = read_pokedex(pokemon_id=id, to_print=False)

        ask_question(mystery_pokemon)
        
        while True:
            user_input = input('>> ').strip().lower()      
            
            if user_input == 'quit':
                return

            if check_answer(
                user_answer=user_input, 
                correct_answer=mystery_pokemon.name
            ):
                print(f"It's...{mystery_pokemon.name.capitalize()}!")
                sleep(1)
                input('\nPress "enter" to continue...')
                break


if __name__ == '__main__':
    setup(PATHS)

    print('''
Welcome to POK\u00e9MON Trivia!

To reveal the answer, enter "help".
To quit the game, enter "quit".

    ''')

    input('Press "enter" to continue...')

    main_loop()

    print('Goodbye.')
