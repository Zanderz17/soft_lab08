from flask import Flask, request, jsonify
from requests.exceptions import RequestException
import requests
import logging
import os
import time

app = Flask(__name__)


def configure_logging():
    log_level = os.environ.get('LOG_LEVEL', 'INFO')
    log_format = '%(asctime)s [%(levelname)s] [%(module_name)s] [%(API)s] [%(funcName)s] %(message)s [%(elapsed_time)s ms]'
    log_filename = 'app.log'

    logging.basicConfig(
        level=log_level,
        format=log_format,
        filename=log_filename,
    )


# Define the base URLs for the three APIs
api_urls = {
    "poke_api": "http://localhost:5001/poke_api",
    "poke_stats": "http://localhost:5003/poke_stats",
    "poke_img": "http://localhost:5002/poke_img"
}

@app.route('/poke_search/<string:pokemon_name>', methods=['GET'])
def poke_search(pokemon_name):
    start_time = time.time()
    logger = logging.getLogger(__name__)

    # Initialize a dictionary to store aggregated data
    aggregated_data = {}

    for api_name, api_url in api_urls.items():
        try:
            response = requests.get(f"{api_url}/{pokemon_name}")
            response.raise_for_status()  # Lanza una excepción si el código de estado HTTP no es 2xx
            data = response.json()
            end_time = time.time()
            elapsed_time = (end_time - start_time) * 1000
            logger.info(f"Se hizo el request correctamente a {api_name}", extra={'module_name': api_name, 'API': f"{api_url}/{pokemon_name}", 'elapsed_time': f'{elapsed_time:.2f}'})
            aggregated_data[api_name] = data
        except RequestException as e:
            # Maneja la excepción de solicitud, que incluye problemas de conexión y errores HTTP
            end_time = time.time()
            elapsed_time = (end_time - start_time) * 1000
            logger.warning(f"Error en el módulo: {api_name}. Descripción: {str(e)}", extra={'module_name': api_name, 'API': f"{api_url}/{pokemon_name}", 'elapsed_time': f'{elapsed_time:.2f}'})
            # Handle errors from individual APIs if needed
            aggregated_data[api_name] = {"error": "Failed to fetch data from API."}

    return jsonify(aggregated_data)

if __name__ == '__main__':
    configure_logging()
    app.run(debug=True, port=5000)