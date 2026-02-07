import logging
import os
import requests
import sys
from pathlib import Path
from PIL import Image
from src.paths import PATHS

logger = logging.getLogger(__name__)

def setup(paths: dict):
    '''Set up directories and logging

    Args:
        paths (dict): Directory paths
    '''
    # Directory paths
    for path in paths.values():
        Path(path).mkdir(parents=True, exist_ok=True)
    
    # Logging
    log_level = os.environ.get('LOG_LEVEL')
    log_path = PATHS['logs'] / f'{os.environ.get('TIMESTAMP')}.log'

    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_path) # save to log file
        ]
    )

    logger.info('Setup complete')
   
def save_cries(pokemon_class: object):
    cries_url = pokemon_class.cries
    response = requests.get(cries_url)

    try:
        response.raise_for_status()
        file_name = f'cries_{pokemon_class.id}_{pokemon_class.name}.ogg'
        output_path = PATHS['cries'] / file_name
        
        with open(output_path, 'wb') as f:
            f.write(response.content)

        logger.info(f'Saved cries for "{pokemon_class.name}"')
    
    except requests.HTTPError as e:
        logger.error(f'Failed to save cries for "{pokemon_class.name}": {e}')
        raise
    
def save_sprites(pokemon_class: object):
    sprites_url = pokemon_class.sprites
    response = requests.get(sprites_url)

    try:
        response.raise_for_status()
        file_name = f'sprites_{pokemon_class.id}_{pokemon_class.name}.png'
        output_path = PATHS['sprites'] / file_name
        
        with open(output_path, 'wb') as f:
            f.write(response.content)

        logger.info(f'Saved sprites for "{pokemon_class.name}"')
    
    except requests.HTTPError as e:
        logger.error(f'Failed to save sprites for "{pokemon_class.name}": {e}')
        raise

def outliner(input_path: object, output_path: object):
    img = Image.open(input_path)

    # Force convert to RGBA
    img = img.convert("RGBA")
    pixels = img.load()

    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = pixels[x, y]
            if a > 0:  # if not transparent
                pixels[x, y] = (0, 0, 0, a)  # turn black, keep alpha

    img.save(output_path)

def load_sprites(pokemon_class: object) -> object:
    id = pokemon_class.id
    name = pokemon_class.name
    
    reveal_file_name = f'sprites_{id}_{name}.png'
    outline_file_name = f'outline_{reveal_file_name}'

    pokemon_class.sprite_reveal_path = PATHS['sprites'] / reveal_file_name
    pokemon_class.sprite_outline_path = PATHS['sprites'] / outline_file_name

    return pokemon_class
