from flask import Flask, send_from_directory, jsonify, request
import os
import time
import logging


app = Flask(__name__)

# Configuración de logging
def configure_logging():
    log_level = os.environ.get('LOG_LEVEL', 'INFO')
    log_format = '%(asctime)s [%(levelname)s] [%(name)s][POKE_IMG][%(funcName)s] %(message)s [%(elapsed_time)s ms]'
    log_filename = 'app.log'

    logging.basicConfig(
        level=log_level,
        format=log_format,
        filename=log_filename,
    )


@app.route('/poke_img/<pokemon_name>')
def serve_pokemon_image(pokemon_name):
    pokemon_name = pokemon_name.capitalize()
    logger = logging.getLogger(__name__)
    
    image_path = f'images/{pokemon_name}/0.jpg'
    start_time = time.time()
    if os.path.exists(image_path):
        response = send_from_directory('images', f'{pokemon_name}/0.jpg')
        end_time = time.time()
        elapsed_time = (end_time - start_time) * 1000
        
        # Obtener la URL de la solicitud actual
        request_url = request.url
        new_request_url = request_url.replace('/poke_img/', '/poke_img/show/')

        logger.info(f"Solicitud exitosa para el Pokémon con nombre: {pokemon_name}", extra={'elapsed_time': f'{elapsed_time:.2f}'})
        
        # Crear un diccionario con la URL y cualquier otro campo personalizado que desees agregar
        response_data = {
            'url': new_request_url
        }
        
        # Convertir el diccionario en una respuesta JSON
        return jsonify(response_data), 200
    else:
        # Manejar el caso en el que no se encuentra el archivo
        end_time = time.time()
        elapsed_time = (end_time - start_time) * 1000
        logger.warning(f"Pokémon no encontrado para el nombre: {pokemon_name}")
        return jsonify({'message': f'Pokémon con nombre "{pokemon_name}" no encontrado'}, extra={'elapsed_time': f'{elapsed_time:.2f}'}), 404

@app.route('/poke_img/show/<pokemon_name>')
def serve_pokemon_image_show(pokemon_name):
    pokemon_name = pokemon_name.capitalize()    
    image_path = f'images/{pokemon_name}/0.jpg'
    if os.path.exists(image_path):
        response = send_from_directory('images', f'{pokemon_name}/0.jpg')
        return response
    else:
        return jsonify({'message': f'Pokémon con nombre "{pokemon_name}" no encontrado'}, extra={'elapsed_time': f'{elapsed_time:.2f}'}), 404


if __name__ == '__main__':
    configure_logging()
<<<<<<< HEAD
    app.run(port=5003)
=======
    app.run(debug = True, port = 5002)
>>>>>>> origin/main
