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

@app.route('/poke_api/<string:name>', methods=['GET'])
def search_pokemon(name):
    logger = logging.getLogger(__name__)
    start_time = time.time()
    pokeapi_url = f'https://pokeapi.co/api/v2/pokemon/{name.lower()}'
    
    try:
        response = requests.get(pokeapi_url)
        end_time = time.time()
        elapsed_time = (end_time - start_time) * 1000
        if response.status_code == 200:
            pokemon_data = response.json()
            logger.info(f"Solicitud exitosa para el Pokémon: {name}", extra={'elapsed_time': f'{elapsed_time:.2f}'})
            return pokemon_data, 200
        else:
            logger.warning(f"Pokémon no encontrado para el pokemon_name: {name}", extra={'elapsed_time': f'{elapsed_time:.2f}'})
            return None  # Pokemon not found or other error
    except requests.exceptions.RequestException as e:
        logger.warning(f"Error al conectarse a la API de Pokemon: ", extra={'elapsed_time': f'{elapsed_time:.2f}'})
        print(f"Error connecting to PokeAPI: {e}")
        return None

if __name__ == '__main__':
    configure_logging()
    app.run(debug=True, port = 5001)
