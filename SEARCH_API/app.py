from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Define the base URLs for the three APIs
api_urls = {
    "poke_api": "http://localhost:5001/poke_api",
    "poke_stats": "http://localhost:5003/poke_stats",
    "poke_img": "http://localhost:5002/poke_img"
}

@app.route('/poke_search/<string:pokemon_name>', methods=['GET'])
def poke_search(pokemon_name):
    if not pokemon_name:
        return jsonify({"error": "Pokemon name is missing."}), 400

    # Initialize a dictionary to store aggregated data
    aggregated_data = {}

    # Fetch data from each API and store it in the dictionary
    for api_name, api_url in api_urls.items():
        response = requests.get(f"{api_url}/{pokemon_name}")
        print(f"{api_url}/{pokemon_name}")
        print("hola")
        print(response)
        if response.status_code == 200:
            print("ga")
            data = response.json()
            aggregated_data[api_name] = data
        else:
            # Handle errors from individual APIs if needed
            aggregated_data[api_name] = {"error": "Failed to fetch data from API."}

    return jsonify(aggregated_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)