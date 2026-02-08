import config
import os
import random
from src.classes import GameStats
from src.paths import PATHS
from src.tall_grass import read_pokedex
from src.utils import setup, load_cry, load_sprites
from term_image.image import from_file
from time import sleep


stats = GameStats()

def get_pokemon() -> object:
    id = random.randint(1, 151)
    pokemon = read_pokedex(pokemon_id=id, to_print=False)
    pokemon = load_sprites(pokemon)
    pokemon = load_cry(pokemon)

    return pokemon

def ask_question(pokemon: object):
    height_ft = round(pokemon.height * 0.328084, 1)
    weight_lb = round(pokemon.weight * 0.2204623, 1)
    ability = random.choice(pokemon.abilities)
    outline_img = from_file(pokemon.sprite_outline_path)

    outline_img.draw()
    title = "Who's that POK\u00e9MON?"
    print()
    print('#' * len(title))
    print(title)
    print('#' * len(title))

    print(f'\n{pokemon.flavor_text}')
    print(f'\n- This POK\u00e9MON is approxiamately {height_ft} ft. tall and weighs about {weight_lb} lb.\n- It is known to have the ability {ability}.\n')

    stats.record_questions()

def check_answer(user_answer: str, correct_answer: str) -> bool:
    user_answer = user_answer

    if user_answer == correct_answer:
        stats.record_correct_answers()
        return True
    elif user_answer == 'answer':
        stats.record_reveals()
        return True
    
    print('Nope try again.')
    return False

def main_loop():
    while True:
        user_input = input('\nPress "enter" to continue...')
        if user_input == 'quit':
            return

        mystery_pokemon = get_pokemon()
        ask_question(mystery_pokemon)
        
        while True:
            user_input = input('>> ').strip().lower()      
            
            if user_input == 'quit':
                return
            elif user_input == 'hint':
                stats.record_hints()
                print(f'\nIts type(s): {", ".join(mystery_pokemon.types)}')
                continue

            if check_answer(
                user_answer=user_input, 
                correct_answer=mystery_pokemon.name
            ):
                reveal_img = from_file(mystery_pokemon.sprite_reveal_path)
                reveal_img.draw()
                print(f"It's...{mystery_pokemon.name.title()}!")
                sleep(0.5)
                os.system(f'ffplay -nodisp -autoexit {mystery_pokemon.cry_path} > /dev/null 2>&1')

                break

            stats.record_wrong_guesses()


if __name__ == '__main__':
    setup(PATHS)

    print('''
Welcome to POK\u00e9MON Trivia!

Enter "hint" to see a hint.
Enter "answer" to reveal the answer.
Enter "quit" to end the game.
    ''')

    main_loop()

    stats.summary()
    print(f'\nGoodbye.')
