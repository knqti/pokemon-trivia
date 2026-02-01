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
    print()
    print('#' * len(title))
    print(title)
    print('#' * len(title))

    print(f'\n{pokemon.flavor_text}')
    print(f'\n- This POK\u00e9MON is approxiamately {height_ft} ft. tall and weighs about {weight_lb} lb.\n- It is known to have the ability {ability}.\n')

def check_answer(user_answer: str, correct_answer: str) -> bool:
    user_answer = user_answer

    if user_answer == correct_answer or user_answer == 'answer':
        return True
    
    print('Nope try again.')
    return False

def main_loop():
    while True:
        user_input = input('\nPress "enter" to continue...')
        if user_input == 'quit':
            return
    
        id = random.randint(1, 151)
        mystery_pokemon = read_pokedex(pokemon_id=id, to_print=False)

        ask_question(mystery_pokemon)
        
        while True:
            user_input = input('>> ').strip().lower()      
            
            if user_input == 'quit':
                return
            elif user_input == 'hint':
                print(f'\nIts type(s): {", ".join(mystery_pokemon.types)}')
                continue

            if check_answer(
                user_answer=user_input, 
                correct_answer=mystery_pokemon.name
            ):
                print(f"It's...{mystery_pokemon.name.title()}!")
                sleep(1)
                break


if __name__ == '__main__':
    setup(PATHS)

    print('''
Welcome to POK\u00e9MON Trivia!

Enter "hint" to see a hint.
Enter "answer" to reveal the answer.
Enter "quit" to end the game.
    ''')

    main_loop()
    print('Goodbye.')
