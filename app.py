from flask import Flask, request, jsonify
import requests
import logging
import os
import time

app = Flask(__name__)

def configure_logging():
    log_level = os.environ.get('LOG_LEVEL', 'INFO')
    log_format = '%(asctime)s [%(levelname)s] [%(name)s][POKE_SEARCH][%(funcName)s] %(message)s [%(elapsed_time)s ms]'
    log_filename = 'app.log'

    logging.basicConfig(
        level=log_level,
        format=log_format,
        filename=log_filename,
    )

# Define the base URLs for the three APIs
api_urls = {
    "poke_info": "http://127.0.0.1:5000/poke_info",
    "poke_stats": "http://127.0.0.1:5001/poke_stats",
    "poke_img": "http://127.0.0.1:5002/poke_img"
}

@app.route('/poke_search/<string:pokemon_name>', methods=['GET'])
def poke_search(pokemon_name):
    start_time = time.time()
    logger = logging.getLogger(__name__)

    if not pokemon_name:
        # Elapsed_time
        end_time = time.time()
        elapsed_time = (end_time - start_time) * 1000
        # Log
        app.logger.error('Falta el parámetro "pokemon_name"', extra={'elapsed_time': f'{elapsed_time:.2f}'})
        return jsonify({"error": "Pokemon name is missing."}), 400

    # Initialize a dictionary to store aggregated data
    aggregated_data = {}

    # Fetch data from each API and store it in the dictionary
    for api_name, api_url in api_urls.items():
        response = requests.get(f"{api_url}/{pokemon_name}")
        if response.status_code == 200:
            data = response.json()
            aggregated_data[api_name] = data
        else:
            end_time = time.time()
            elapsed_time = (end_time - start_time) * 1000
            logger.warning(f"Pokémon no encontrado para el pokemon_name: {pokemon_name}", extra={'elapsed_time': f'{elapsed_time:.2f}'})
            # Handle errors from individual APIs if needed
            aggregated_data[api_name] = {"error": "Failed to fetch data from API."}

    # Elapsed_time 
    end_time = time.time()
    elapsed_time = (end_time - start_time) * 1000
    logger.info(f"Solicitud exitosa para el Pokémon: {pokemon_name}", extra={'elapsed_time': f'{elapsed_time:.2f}'})
    return jsonify(aggregated_data)

if __name__ == '__main__':
    app.run(port=5000)