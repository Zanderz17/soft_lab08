from flask import Flask, jsonify, request
import psycopg2
import logging
import os
import time

app = Flask(__name__)

# Configuración de la base de datos
db_params = {
    'dbname': 'Soft_Semana08',
    'user': 'postgres',
    'password': '161049',
    'host': 'localhost',  # Cambia esto si tu base de datos está en otro servidor
    'port': '5432'        # El puerto por defecto de PostgreSQL es 5432
}

# Configuración de logging
def configure_logging():
    log_level = os.environ.get('LOG_LEVEL', 'INFO')
    log_format = '%(asctime)s [%(levelname)s] [%(name)s][POKE_STATS][%(funcName)s] %(message)s [%(elapsed_time)s ms]'
    log_filename = 'app.log'

    logging.basicConfig(
        level=log_level,
        format=log_format,
        filename=log_filename,
    )

# Ruta para obtener datos de un Pokémon por Name
@app.route('/poke_stats/<string:name>', methods=['GET'])
def get_pokemon_by_name(name):
    # Conexión a la base de datos
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    # Registra el tiempo en que se ejecuta la consulta
    start_time = time.time()

    # Ejecutar una consulta SQL para obtener los datos del Pokémon por Name
    cursor.execute("SELECT * FROM Pokemon_Stats WHERE Name = %s", (name,))
    data = cursor.fetchone()

    # Calcular el tiempo transcurrido en milisegundos
    end_time = time.time()
    elapsed_time = (end_time - start_time) * 1000

    # Cerrar la conexión
    cursor.close()
    conn.close()

    # Configura el registro dentro de la función
    logger = logging.getLogger(__name__)
    if data:
        # Crear un diccionario con los datos del Pokémon
        pokemon = {
            'poke_id': data[1],
            'Name': data[2],
            'Type_1': data[3],
            'Type_2': data[4],
            'Total': data[5],
            'HP': data[6],
            'Attack': data[7],
            'Defense': data[8],
            'Sp_Atk': data[9],
            'Sp_Def': data[10],
            'Speed': data[11],
            'Generation': data[12],
            'Legendary': data[13]
        }
        # Registra un mensaje de log indicando la solicitud exitosa
        logger.info(f"Solicitud exitosa para el Pokémon con Name: {name}", extra={'elapsed_time': f'{elapsed_time:.2f}'})
        return jsonify(pokemon)
    else:
        # Registra un mensaje de log indicando que el Pokémon no fue encontrado
        logger.warning(f"Pokémon no encontrado para el Name: {name}", extra={'elapsed_time': f'{elapsed_time:.2f}'})
        return jsonify({'message': f'Pokémon con Name "{name}" no encontrado'}), 404

if __name__ == '__main__':
    configure_logging()
    app.run(debug=True)
