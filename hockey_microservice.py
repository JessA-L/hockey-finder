import os
import json
from time import sleep

# must have a txt file with the text 'run' to properly run this microservice
command_path = 'microservice_command.txt'


def update_json():
    """
    Pulls information from tm-results.json and updates the soonest/cheapest lists
    to reflect the proper events to update microservice_results.json with.
    microservice_results.json holds a list with [0] being a nested list with all
    the soonest games while [1] is a nested list with all the cheapest games.
    If 'priceRanges' is not within the event information then only soonest games
    will be updated while [1] for cheapest will be an empty nested list.
    :return: None
    """
    if command == "run":
        #
        with open('tm-results.json', 'r') as tm_results:
            event_info = json.load(tm_results)

        soonest = []
        cheapest = []

        # updates soonest/cheapest by redefining or appending if values match
        events = event_info["_embedded"]["events"]
        for event in events:
            name = event['name']
            date = event['dates']['start']['localDate']
            if 'priceRanges' in event:
                lowest_price = event['priceRanges'][0]['min']
                print("Date: " + date + " Price: " + str(lowest_price) + " " + name)
            else:
                print("Date: " + date + " " + name)
            if not soonest:
                soonest = [event]
            else:
                if date < soonest[0]['dates']['start']['localDate']:
                    soonest = [event]
                elif date == soonest[0]['dates']['start']['localDate']:
                    soonest.append(event)

            if 'priceRanges' in event:
                if not cheapest:
                    cheapest = [event]
                else:
                    if lowest_price < cheapest[0]['priceRanges'][0]['min']:
                        cheapest = [event]
                    elif lowest_price == cheapest[0]['priceRanges'][0]['min']:
                        cheapest.append(event)

        # outputs relevant event information to terminal
        print()
        for event in soonest:
            print(f'Soonest is {event["name"]} at {event["dates"]["start"]["localDate"]}')
        if cheapest:
            for event in cheapest:
                print(f'Cheapest is {event["name"]} at {event["priceRanges"][0]["min"]}')
        print('\n')

        # updates microservice_results with nested lists of soonest/cheapest events
        with open('microservice_results', 'w') as ms_results:
            soonest_cheapest = [soonest, cheapest]
            ms_results.write(json.dumps(soonest_cheapest))

        # overwrites microservice_command.txt
        with open(command_path, 'w') as outfile:
            outfile.write('')


while True:
    # Checks if path exists to the command file which should be
    # updated with run when this service is to run
    if os.path.exists(command_path):
        with open(command_path, 'r') as openfile:
            command = openfile.readline()
        update_json()
    sleep(1)
