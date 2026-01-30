import config
import random
from src.paths import PATHS
from src.tall_grass import read_pokedex
from src.utils import setup


def ask_question(pokemon: object):
    height_ft = round(pokemon.height * 0.328084, 1)
    weight_lb = round(pokemon.weight * 0.2204623, 1)
    ability = random.choice(pokemon.abilities)
    title = "Who's that Pokemon?"

    print('#' * len(title))
    print(title)
    print('#' * len(title))

    print(f'\n- This Pokemon is approxiamately {height_ft} ft. tall and weighs about {weight_lb} lb.\n- It is known to have the ability {ability}.\n')
    print(mystery_pokemon.flavor_text)

def check_answer(user_answer: str, correct_answer: str) -> bool:
    user_answer = user_answer.strip().lower()

    if user_answer == correct_answer:
        print('Correct!')
        return True
    elif user_answer == 'help':
        return True
    
    print('Nope try again.')
    return False


if __name__ == '__main__':
    setup(PATHS)

    id = random.randint(1, 151)
    mystery_pokemon = read_pokedex(pokemon_id=id, to_print=False)
    ask_question(mystery_pokemon)

    flag = False
    while flag == False:
        user_input = input('>> ')
        flag = check_answer(
            user_answer=user_input, 
            correct_answer=mystery_pokemon.name
        )

    print(f"It's...{mystery_pokemon.name.capitalize()}!")
