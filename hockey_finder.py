import json
import tkinter as tk
from time import sleep
import requests
import zmq

bg_color = "#3D6466"

def load_results_frame(results_frame):
    """
    Initiates response to search button click.
    Used by ui().
    :return: None
    :params: None
    """
    results_frame.tkraise()

    input_city = tk.StringVar()
    input_city.set(city_input_box.get())
    print(input_city.get())

    call_ticketmaster(input_city.get())
                
    # Print results in CLI
    output_results()
    
    # Print closest and soonest games in CLI
    print("\nCheapest and soonest:")
    get_cheapest_and_soonest()
    
def load_welcome_frame(welcome_frame, results_frame) -> None:
        
    welcome_frame.tkraise()            
    welcome_frame.pack_propagate(False)
    
    # create welcome frame widgets
    welcome_title = tk.Label(
        welcome_frame, 
        text="Hockey Finder",
        bg=bg_color,
        fg="white",
        font=("TkMenuFont", 26)
        )
    
    welcome_desc = tk.Label(
        welcome_frame, 
        text="Find a hockey game near you!",
        bg=bg_color,
        fg="white",
        font=("TkMenuFont", 14)
        )
    
    city_text = tk.Label(
        welcome_frame, 
        text="Input city: ",
        bg=bg_color,
        fg="white",
        font=("TkMenuFont", 14)
        ) 
    global city_input_box
    city_input_box = tk.Entry(welcome_frame, 
        width=10
        )
    
    search_button = tk.Button(welcome_frame, 
        text="Search", 
        font=("TkHeadingFont", 20),
        bg="darkred",
        fg="white",
        cursor="hand2",
        activebackground="#BADEE2",
        activeforeground="black",
        command=lambda:load_results_frame(results_frame)
        ) 
    
    # Display welcome widgets
    welcome_title.pack(pady=20)
    welcome_desc.pack(pady=10)
    city_text.pack(pady=5)
    city_input_box.pack(pady=5)
    search_button.pack(pady=5)

def gui() -> None:
    """
    Generates gui.
    """
    # initiallize app
    root = tk.Tk()
    root.title("Hockey Finder")
    root.eval("tk::PlaceWindow . center")
    
    # create a frame widget
    welcome_frame = tk.Frame(root, width=500, height=600, bg=bg_color)
    results_frame = tk.Frame(root, bg=bg_color)
    
    for frame in (welcome_frame, results_frame):
        frame.grid(row=0, column=0)
    
    load_welcome_frame(welcome_frame, results_frame)
    
    # Create loop
    root.mainloop()
    
def output_results() -> None:
    """
    Prints results in terminal.
    """
    with open('tm-results.json', 'r') as infile:
        test_data = json.load(infile)
    for i in range(10):
        print(test_data["_embedded"]["events"][i]["name"] + " " + test_data["_embedded"]["events"][i]["dates"]["start"]["localDate"])

def get_cheapest_and_soonest():
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
    
    return soonest, cheapest
            
def call_ticketmaster(city): 
    # Set the API ENDPOINT and API key
    ENDPOINT = "https://app.ticketmaster.com/discovery/v2/events.json"
    API_KEY = "XSsjkkAUauyyZ0nRH5AxLkWXNs3JTLNY"

    # Set the search parameters
    params = {
        "apikey": API_KEY,
        "keyword": "hockey", 
        "city": city, 
        "radius": 100,
        "size": 10,
    }

    # Make the API call
    response = requests.get(ENDPOINT, params=params)

    # Output the response to a JSON file
    event_list = response.json()
    with open('tm-results.json', 'w') as outfile:
        json.dump(event_list, outfile)
        
if __name__ == "__main__":
    gui()
