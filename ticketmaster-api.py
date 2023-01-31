# Program makes API call to ticketmaster

import requests
import json

# Set the API ENDPOINT and API key
ENDPOINT = "https://app.ticketmaster.com/discovery/v2/events.json"
API_KEY = "XSsjkkAUauyyZ0nRH5AxLkWXNs3JTLNY"

while True:
    # get user input from text file
    infile = open('zip-code.txt', 'r')
    zipCode = infile.readline()
    
    # Check for zipcode or "DONE"
    if zipCode.isnumeric():    
        zipCode = int(zipCode)

        # Set the search parameters
        params = {
            "apikey": API_KEY,
            "keyword": "hockey", 
            # "city": city, 
            "postalCode": zipCode,
            "radius": 100,
            "size": 10,
        }

        # Make the API call
        response = requests.get(ENDPOINT, params=params)

        # Output the response to a JSON file
        event_list = response.json()
        with open('tm-results.json', 'w') as outfile:
            json.dump(event_list, outfile)
        