import requests

base_url = "https://pokeapi.co/api/v2"

def get_pokemon_info(name):
    url = f"{base_url}/pokemon/{name.lower()}"
    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Data not retrieved: {response.status_code}")
        return None

pokemon_name = "pikachu"
pokemon_info = get_pokemon_info(pokemon_name)

if pokemon_info:
    print(f"Name: {pokemon_info['name'].capitalize()}")
    print(f"Id: {pokemon_info['id']}")
    print(f"Height: {pokemon_info['height']}")
    print(f"Weight: {pokemon_info['weight']}")
