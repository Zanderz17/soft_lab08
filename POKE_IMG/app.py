from flask import Flask, send_from_directory
import os
import time
import logging


app = Flask(__name__)

# Configuración de logging
def configure_logging():
    log_level = os.environ.get('LOG_LEVEL', 'INFO')
    log_format = '%(asctime)s [%(levelname)s] [%(name)s][POKE_IMG][%(funcName)s] %(message)s'
    log_filename = 'app.log'

    logging.basicConfig(
        level=log_level,
        format=log_format,
        filename=log_filename,
    )


@app.route('/poke_img/<pokemon_name>')
def serve_pokemon_image(pokemon_name):
    # Convertir la primera letra a mayúscula y el resto a minúsculas

    pokemon_name = pokemon_name.capitalize()
    logger = logging.getLogger(__name__)
    try:
        # Servir la imagen desde la ruta del archivo
        logger.info(f"Solicitud exitosa para el Pokémon con nombre: {pokemon_name}")
        return send_from_directory('images', f'{pokemon_name}/0.jpg')
    except FileNotFoundError:
        # Manejar el caso en el que no se encuentra el archivo
        return 'Imagen no encontrada', 404

if __name__ == '__main__':
    configure_logging()
    app.run(port=5001)
