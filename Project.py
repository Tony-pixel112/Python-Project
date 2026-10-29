import requests

# 1. The API endpoint (the "waiter's address")
url = "https://official-joke-api.appspot.com/random_joke"

print("Sending request to the API server...")

# 2. Make the request (the waiter goes to fetch the data)
response = requests.get(url)

# 3. Convert the server's response into a readable Python dictionary (JSON format)
joke_data = response.json()

# 4. Print out the results delivered by the API
print("\n🎉 Success! Here is what the API brought back:")
print(f"Setup: {joke_data['setup']}")
print(f"Punchline: {joke_data['punchline']}")