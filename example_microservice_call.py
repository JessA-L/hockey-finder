import json
import zmq


with open('tm-results.json', 'r') as tm_results:
    event_info = json.load(tm_results)

context = zmq.Context()

# socket to talk to server
print("Connecting to microservice server...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

# send request to soonest/cheapest microservice
print("Sending request to microservice...")
socket.send_json(event_info)

# Get the reply
soonest_cheapest = socket.recv_json()
print(f"Received reply...")


# Example print for the games returned
soonest = soonest_cheapest[0]
cheapest = soonest_cheapest[1]
print()
print('Soonest games:')
for event in soonest:
    print(f'{event["name"]} at {event["dates"]["start"]["localDate"]}')
if cheapest:
    print('Cheapest games:')
    for event in cheapest:
        print(f'{event["name"]} at {event["priceRanges"][0]["min"]}')

