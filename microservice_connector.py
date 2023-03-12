import zmq
import json

def connect_to_microservice():
    context = zmq.Context()

    # socket to talk to server
    print("Connecting to microservice server...")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    return socket

def microservice_call(socket):
    with open('tm-results.json', 'r') as tm_results:
        event_info = json.load(tm_results)

    # send request to soonest/cheapest microservice
    print("Sending request to microservice...")
    socket.send_json(event_info)

    # Get the reply
    print(f"Received reply...")
    return socket.recv_json()
