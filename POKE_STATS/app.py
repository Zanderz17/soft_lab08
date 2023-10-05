from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

# Configuración de la base de datos
db_params = {
    'dbname': 'Soft_Semana08',
    'user': 'postgres',
    'password': '161049',
    'host': 'localhost',  # Cambia esto si tu base de datos está en otro servidor
    'port': '5432'        # El puerto por defecto de PostgreSQL es 5432
}

# Ruta para obtener datos de un Pokémon por poke_id
@app.route('/poke_stats/<int:poke_id>', methods=['GET'])
def get_pokemon_by_id(poke_id):
    # Conexión a la base de datos
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    # Ejecutar una consulta SQL para obtener los datos del Pokémon por poke_id
    cursor.execute("SELECT * FROM Pokemon_Stats WHERE poke_id = %s", (poke_id,))
    data = cursor.fetchone()

    # Cerrar la conexión
    cursor.close()
    conn.close()

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
        return jsonify(pokemon)
    else:
        return jsonify({'message': 'Pokémon no encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)
