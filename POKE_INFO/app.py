from flask import Flask, request, jsonify
import requests
import logging
import os
import time

app = Flask(__name__)

def configure_logging():
    log_level = os.environ.get('LOG_LEVEL', 'INFO')
    log_format = '%(asctime)s [%(levelname)s] [%(name)s][POKE_INFO][%(funcName)s] %(message)s [%(elapsed_time)s ms]'
    log_filename = 'app.log'

    logging.basicConfig(
        level=log_level,
        format=log_format,
        filename=log_filename,
    )

@app.route('/poke/search', methods=['GET'])
def search_pokemon():
    pokemon_name = request.args.get('pokemon_name')
    start_time = time.time()
    logger = logging.getLogger(__name__)

    if not pokemon_name:
        # Elapsed_time 
        end_time = time.time()
        elapsed_time = (end_time - start_time) * 1000
        # Log
        app.logger.error('Falta el parámetro "pokemon_name"', extra={'elapsed_time': f'{elapsed_time:.2f}'})
        return jsonify({'error': 'Missing "pokemon_name" parameter'}), 400


    # Call your PokeAPI Manager function to fetch data
    pokemon_data = get_pokemon_data(pokemon_name)
    # Elapsed_time 
    end_time = time.time()
    elapsed_time = (end_time - start_time) * 1000

    if pokemon_data:
        logger.info(f"Solicitud exitosa para el Pokémon: {pokemon_name}", extra={'elapsed_time': f'{elapsed_time:.2f}'})
        return jsonify(pokemon_data)
    else:
        logger.warning(f"Pokémon no encontrado para el pokemon_name: {pokemon_name}", extra={'elapsed_time': f'{elapsed_time:.2f}'})
        return jsonify({'error': 'Pokemon not found'}), 404


def get_pokemon_data(pokemon_name):
    pokeapi_url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}'

    try:
        response = requests.get(pokeapi_url)

        if response.status_code == 200:
            pokemon_data = response.json()
            return pokemon_data
        else:
            return None  # Pokemon not found or other error
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to PokeAPI: {e}")
        return None


if __name__ == '__main__':
    configure_logging()
    app.run(debug=True)
