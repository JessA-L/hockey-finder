import json
import tkinter as tk
import requests
import microservice_connector

bg_color = "#393e46"


def gui() -> None:
    """
    Generates gui.
    """
    # initialize app
    root = tk.Tk()
    root.title("Hockey Finder")
    root.eval("tk::PlaceWindow . center")

    # create frame widgets
    welcome_frame = tk.Frame(root, width=650, height=850, bg=bg_color)
    results_frame = tk.Frame(root, bg=bg_color)

    for frame in (welcome_frame, results_frame):
        frame.grid(row=0, column=0)

    load_welcome_frame(welcome_frame, results_frame)

    root.mainloop()


def load_welcome_frame(welcome_frame, results_frame) -> None:
    """
    Creates and displays welcome frame
    """
    welcome_frame.tkraise()
    welcome_frame.pack_propagate(False)

    # displays welcome frame widgets
    welcome_frame_widgets(welcome_frame, results_frame)


def title(welcome_frame):
    """
    Create and display title
    Used by welcome_frame_widgets()
    """
    welcome_title = tk.Label(
        welcome_frame,
        text="Hockey Finder",
        bg=bg_color,
        fg="red",
        font=("TkMenuFont", 28)
    )
    welcome_title.pack(pady=20)


def description(welcome_frame):
    """
    Create and display description
    Used by welcome_frame_widgets()
    """
    welcome_desc = tk.Label(
        welcome_frame,
        text="Find a hockey game near you!",
        bg=bg_color,
        fg="white",
        font=("TkMenuFont", 16)
    )
    welcome_desc.pack(pady=10)


def instructions(welcome_frame):
    """
    Create and display instructions
    Used by welcome_frame_widgets()
    """
    city_text = tk.Label(
        welcome_frame,
        text="Select either team or city.\n Then, input the name of the team or city you would like to search.",
        bg=bg_color,
        fg="white",
        font=("TkMenuFont", 12)
    )
    city_text.pack(pady=5)


def radio_buttons(welcome_frame):
    """
    Create and display radio buttons
    Used by welcome_frame_widgets()
    """
    global radio_sel
    radio_sel = tk.StringVar()
    radio_team = tk.Radiobutton(welcome_frame,
                                text="Search by Team",
                                variable=radio_sel,
                                value="keyword"
                                )
    radio_team.pack(pady=5)

    radio_city = tk.Radiobutton(welcome_frame,
                                text="Search by City",
                                variable=radio_sel,
                                value="city"
                                )
    radio_city.pack(pady=5)


def input_box(welcome_frame) -> None:
    """
    Create and display input box
    Used by welcome_frame_widgets()
    """
    global input_box
    input_box = tk.Entry(welcome_frame,
                         width=10
                         )
    input_box.pack(pady=5)


def search_button(welcome_frame, results_frame) -> None:
    """
    Create and display search button
    Used by welcome_frame_widgets()
    """
    search_button = tk.Button(welcome_frame,
                              text="Search",
                              font=("TkHeadingFont", 20),
                              bg="red",
                              fg="white",
                              cursor="hand2",
                              activebackground="#BADEE2",
                              activeforeground="black",
                              command=lambda: load_results(results_frame)
                              )
    search_button.pack(pady=5)


def welcome_frame_widgets(welcome_frame, results_frame) -> None:
    """
    Display widgets on welcome frame
    Used by load_welcome_frame()
    """
    title(welcome_frame)
    description(welcome_frame)
    instructions(welcome_frame)
    radio_buttons(welcome_frame)
    input_box(welcome_frame)
    search_button(welcome_frame, results_frame)


def get_radio_sel() -> str:
    """
    Gets input from radio selection
    Used by load_results()
    """
    radio_selected = radio_sel.get()
    return radio_selected


def get_box_input() -> str:
    """
    Gets input from text box.
    Used by load_results()
    """
    box_input_var = tk.StringVar()
    box_input_var.set(input_box.get())
    box_input = box_input_var.get()

    return box_input


def load_results(results_frame) -> None:
    """
    Creates results frame, calls ticketmaster API, displays cheapest and soonest games in GUI
    Used by search_button()
    """
    results_frame.tkraise()
    call_ticketmaster(get_radio_sel(), get_box_input())

    soonest, cheapest = get_cheapest_and_soonest()
    tk.Label(
        results_frame,
        text=f'Soonest Game: {soonest[0]["name"]} on {soonest[0]["dates"]["start"]["localDate"]}\n'
             f'Cheapest Game: {cheapest[0]["name"]} at {cheapest[0]["priceRanges"][0]["min"]}',
        bg=bg_color,
        fg="white",
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
    Used by load_results()
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
