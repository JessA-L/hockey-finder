import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    event_info = socket.recv_json()
    print("Received request for soonest/cheapest game data...")

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
    print('Soonest games:')
    for event in soonest:
        print(f'{event["name"]} at {event["dates"]["start"]["localDate"]}')
    if cheapest:
        print('Cheapest games:')
        for event in cheapest:
            print(f'{event["name"]} at {event["priceRanges"][0]["min"]}')

    # sends nested lists of soonest and cheapest games
    soonest_cheapest = [soonest, cheapest]
    socket.send_json(soonest_cheapest)
    print("Sending results...")
