# A GUI that receives user input. When input is entered...
    # UI calls the ticketmaster service
    # UI displays the search results

import json
from tkinter import *
from time import sleep
import json
import zmq

class GraphicalUserInterface(object):
    def __init__(self) -> None:
        super().__init__()
                   
    def gui(self) -> None:
        """
        Generates gui.
        """
        def my_click():
            """
            Initiates response to search button click.
            Used by ui().
            :return: None
            :params: None
            """
            input_city = city_input_box.get()
            print(input_city)

            with open('zip-code.txt', 'w') as outfile:
                outfile.write(input_city)
            
            # Print results in CLI
            sleep(2)
            self.output_results()
            
            # Print closest and soonest games in CLI
            print("\nClosest and soonest:")
            self.get_closest_and_soonest()
            
            # Reset program
            with open('zip-code.txt', 'w') as outfile:
                outfile.write("DONE")

        # Create widgets
        root = Tk()
        title = Label(root, text="Hockey Finder")
        description = Label(root, text="Find a hockey game near you: ")
        city_label = Label(root, text="Zip Code: ")
        city_input_box = Entry(root, width=10)
        search_button = Button(root, text="Search", command=my_click, fg="white", bg="darkred")

        # Put widget onto the screen
        title.grid(row=0, column=1)
        description.grid(row=1, column=1)
        city_label.grid(row=2, column=0)
        city_input_box.grid(row=2, column=1)
        search_button.grid(row=2, column=2)

        # Create loop
        root.mainloop()
        
    def output_results(self) -> None:
        """
        Prints results in terminal.
        """
        with open('tm-results.json', 'r') as infile:
            test_data = json.load(infile)
        for i in range(10):
            print(test_data["_embedded"]["events"][i]["name"] + " " + test_data["_embedded"]["events"][i]["dates"]["start"]["localDate"])

    def get_closest_and_soonest(self):
        """
        Uses microservice to get the closest and soonest hockey games from provided dictionary.
        """
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

widg = GraphicalUserInterface()
widg.gui()
