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
    welcome_frame.tkraise()
    welcome_frame.pack_propagate(False)

    # creates and displays welcome frame widgets
    welcome_frame_widgets(welcome_frame, results_frame)


def display_welcome_title(welcome_frame):
    welcome_title = tk.Label(
        welcome_frame,
        text="Hockey Finder",
        bg=bg_color,
        fg="red",
        font=("TkMenuFont", 28)
    )
    welcome_title.pack(pady=20)


def display_welcome_desc(welcome_frame):
    welcome_desc = tk.Label(
        welcome_frame,
        text="Find a hockey game near you!",
        bg=bg_color,
        fg="white",
        font=("TkMenuFont", 16)
    )
    welcome_desc.pack(pady=10)


def display_city_text(welcome_frame):
    city_text = tk.Label(
        welcome_frame,
        text="Select either team or city.\n Then, input the name of the team or city you would like to search.",
        bg=bg_color,
        fg="white",
        font=("TkMenuFont", 12)
    )
    city_text.pack(pady=5)


def display_radios(welcome_frame):
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


def get_radio_sel() -> str:
    radio_selected = radio_sel.get()
    return radio_selected


def display_input_box(welcome_frame) -> None:
    global input_box
    input_box = tk.Entry(welcome_frame,
                         width=10
                         )
    input_box.pack(pady=5)


def display_search_button(welcome_frame, results_frame) -> None:
    search_button = tk.Button(welcome_frame,
                              text="Search",
                              font=("TkHeadingFont", 20),
                              bg="red",
                              fg="white",
                              cursor="hand2",
                              activebackground="#BADEE2",
                              activeforeground="black",
                              command=lambda: load_city_results(results_frame)
                              )
    search_button.pack(pady=5)


def welcome_frame_widgets(welcome_frame, results_frame) -> None:
    """"""
    display_welcome_title(welcome_frame)
    display_welcome_desc(welcome_frame)
    display_city_text(welcome_frame)
    display_radios(welcome_frame)
    display_input_box(welcome_frame)
    display_search_button(welcome_frame, results_frame)


def get_box_input() -> str:
    box_input_var = tk.StringVar()
    box_input_var.set(input_box.get())
    box_input = box_input_var.get()

    return box_input


def load_city_results(results_frame) -> None:
    results_frame.tkraise()

    call_ticketmaster(get_radio_sel(), get_box_input())

    # Display soonest game in ui
    soonest, cheapest = get_cheapest_and_soonest()
    tk.Label(
        results_frame,
        text=f'Soonest Game: {soonest[0]["name"]} on {soonest[0]["dates"]["start"]["localDate"]}\n'
             f'Cheapest Game: {cheapest[0]["name"]} at {cheapest[0]["priceRanges"][0]["min"]}',
        bg=bg_color,
        fg="white",
        font=("TkMenuFont", 12)
    ).pack()


def get_cheapest_and_soonest():
    """
    Connects to hockey microservice using zeroMQ, sends a request containing hockey games,
    and returns the soonest and cheapest games.
    """
    socket = microservice_connector.connect_to_microservice()
    reply = microservice_connector.microservice_call(socket)
    soonest, cheapest = reply[0], reply[1]

    return soonest, cheapest


def call_ticketmaster(radio_choice, search_input):
    """
    Calls ticketmaster API using user provided search parameters and writes results into a JSON file.
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
