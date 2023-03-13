import json
import tkinter as tk
import requests
import microservice_connector


def gui() -> None:
    """
    Generates gui.
    """
    # initialize app
    root = tk.Tk()
    root.title("Hockey Finder")
    root.eval("tk::PlaceWindow . center")

    # create frame widgets
    global welcome_frame
    global results_frame
    welcome_frame = tk.Frame(root, width=850, height=900)
    results_frame = tk.Frame(root)

    for frame in (welcome_frame, results_frame):
        frame.grid(row=0, column=0)

    load_welcome_frame()

    root.mainloop()


def load_welcome_frame() -> None:
    """
    Creates and displays welcome frame
    """
    welcome_frame.tkraise()
    welcome_frame.pack_propagate(False)

    # displays welcome frame widgets
    welcome_frame_widgets()


def title():
    """
    Create and display title
    Used by welcome_frame_widgets()
    """
    welcome_title = tk.Label(
        welcome_frame,
        text="Hockey Finder",
        fg="red",
        font=("TkMenuFont", 28)
    )
    welcome_title.pack(pady=20)


def description():
    """
    Create and display description
    Used by welcome_frame_widgets()
    """
    welcome_desc = tk.Label(
        welcome_frame,
        text="Find a hockey game near you!",
        font=("TkMenuFont", 16)
    )
    welcome_desc.pack(pady=10)


def instructions():
    """
    Create and display instructions
    Used by welcome_frame_widgets()
    """
    city_text = tk.Label(
        welcome_frame,
        text="Select either team or city.\n Then, input the name of the team or city you would like to search.",
        font=("TkMenuFont", 12)
    )
    city_text.pack(pady=5)


def radio_buttons():
    """
    Create and display radio buttons
    Used by welcome_frame_widgets()
    """
    global radio_sel
    radio_sel = tk.StringVar()
    radio_team = tk.Radiobutton(welcome_frame,
                                text="Search by Team",
                                variable=radio_sel,
                                value="keyword",
                                font=("TkMenuFont", 10)
                                )
    radio_team.pack(pady=5)

    radio_city = tk.Radiobutton(welcome_frame,
                                text="Search by City",
                                variable=radio_sel,
                                value="city",
                                font=("TkMenuFont", 10)
                                )
    radio_city.pack(pady=5)


def input_box() -> None:
    """
    Create and display input box
    Used by welcome_frame_widgets()
    """
    global input_box
    input_box = tk.Entry(welcome_frame,
                         width=10
                         )
    input_box.pack(pady=5)


def search_button() -> None:
    """
    Create and display search button
    Used by welcome_frame_widgets()
    """
    search_button = tk.Button(welcome_frame,
                              text="Search",
                              font=("TkHeadingFont", 20),
                              bg="red",
                              cursor="hand2",
                              activebackground="#BADEE2",
                              activeforeground="black",
                              command=lambda: load_results_frame()
                              )
    search_button.pack(pady=5)


def welcome_frame_widgets() -> None:
    """
    Display widgets on welcome frame
    Used by load_welcome_frame()
    """
    title()
    description()
    instructions()
    radio_buttons()
    input_box()
    search_button()


def get_radio_sel() -> str:
    """
    Gets input from radio selection
    Used by load_results_frame()
    """
    radio_selected = radio_sel.get()
    return radio_selected


def get_box_input() -> str:
    """
    Gets input from text box.
    Used by load_results_frame()
    """
    box_input_var = tk.StringVar()
    box_input_var.set(input_box.get())
    box_input = box_input_var.get()

    return box_input


def load_results_frame() -> None:
    """
    Creates results frame, calls ticketmaster API, displays cheapest and soonest games in GUI
    Used by search_button()
    """
    results_frame.tkraise()
    call_ticketmaster(get_radio_sel(), get_box_input())

    load_results()


def load_results():
    """
    Display results from microservice call
    Used by load_results_frame
    """
    soonest, cheapest = get_cheapest_and_soonest()

    if soonest:
        soonest_text = f'Soonest Game: {soonest[0]["name"]} on {soonest[0]["dates"]["start"]["localDate"]}\n'
    else:
        soonest_text = "Error: cannot find soonest game"
    if cheapest:
        cheapest_text = f'Cheapest Game: {cheapest[0]["name"]} at {cheapest[0]["priceRanges"][0]["min"]}\n'
    else:
        cheapest_text = "Error: cannot find cheapest game"

    tk.Label(
        results_frame,
        text=f'{soonest_text}\n{cheapest_text}',
        font=("TkMenuFont", 12)
    ).pack()

def get_cheapest_and_soonest() -> json:
    """
    Connects to hockey microservice using zeroMQ, sends a request containing hockey games,
    and returns the soonest and cheapest games.
    Used by load_results()
    """
    socket = microservice_connector.connect_to_microservice()
    reply = microservice_connector.microservice_call(socket)
    soonest, cheapest = reply[0], reply[1]

    return soonest, cheapest


def call_ticketmaster(radio_choice, search_input):
    """
    Calls ticketmaster API using user provided search parameters and writes results into a JSON file.
    Used by load_results_frame()
    """
    endpoint = "https://app.ticketmaster.com/discovery/v2/events.json"
    api_key = "XSsjkkAUauyyZ0nRH5AxLkWXNs3JTLNY"

    params = {
        "apikey": api_key,
        "keyword": "hockey",
        radio_choice: search_input,
        "radius": 100,
        "size": 10,
    }

    response = requests.get(endpoint, params=params)

    event_list = response.json()
    with open('tm-results.json', 'w') as outfile:
        json.dump(event_list, outfile)


if __name__ == "__main__":
    gui()
