from pathlib import Path

root_dir = Path(__file__).parent.parent
PATHS = {
    'logs': root_dir / 'logs',
    'cries': root_dir / 'pokedex' / 'cries',
    'pokemon': root_dir / 'pokedex' / 'pokemon',
    'sprites': root_dir / 'pokedex' / 'sprites',
}
