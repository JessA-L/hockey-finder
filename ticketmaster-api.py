import requests
import json

# Set the API endpoint and your API key
endpoint = "https://app.ticketmaster.com/discovery/v2/events.json"
api_key = "XSsjkkAUauyyZ0nRH5AxLkWXNs3JTLNY"

# get user input
# city = input("City: ")
zipCode = input("Zip Code: ")

# Set the search parameters
params = {
    "apikey": api_key,
    "keyword": "hockey", 
    # "city": city, 
    "postalCode": zipCode,
    "radius": 100,
    "size": 10,
}

# Make the API call
response = requests.get(endpoint, params=params)

# Output the response to a JSON file
event_list = response.json()
with open('tm-results.json', 'w') as outfile:
    json.dump(event_list, outfile)

