import requests
import json

# Set the API endpoint and your API key
ENDPOINT = "events"
url = f"https://api.seatgeek.com/2/{ENDPOINT}"
CLIENT_ID = "MzA1MjU0ODZ8MTY3NTA5MDE4MS43OTU5NDI"
CLIENT_SECRET = "4ceb......."

# get user input
# city = input("City: ")
# zipCode = input("Zip Code: ")

# Set the search parameters
params = {
    "client_id": CLIENT_ID,
    # "type": "hockey",
    "postal_code": "10001",
    # "datetime_utc": "2023-02-08",
}

# Make the API call
response = requests.get(url=url, params=params)

# Output the response to a JSON file
event_list = response.json()
with open('sg-results.json', 'w') as outfile:
    json.dump(event_list, outfile)

