# A GUI that receives user input. When input is entered...
    # UI calls the ticketmaster service
    # UI displays the search results

import json
from tkinter import *
from time import sleep
import json
import zmq

class gui():
    def __init__(self) -> None:
        super().__init__()
                   
    def ui(self) -> None:
        """
        Generates gui.
        """
        def myClick():
            """
            Initiates response to search button click.
            Used by ui().
            :return: None
            :params: None
            """
            # get input zip from zipEntry box
            inputZip = zipEntry.get()
            print(inputZip)

            # write zipcode to file
            with open('zip-code.txt', 'w') as outfile:
                outfile.write(inputZip)
            
            # Print results in CLI
            sleep(2)
            self.outputResults()
            
            # Reset program
            with open('zip-code.txt', 'w') as outfile:
                outfile.write("DONE")

        # Create widgets
        root = Tk()
        title = Label(root, text="Hockey Finder")
        description = Label(root, text="Find a hockey game near you: ")
        zipCode = Label(root, text="Zip Code: ")
        zipEntry = Entry(root, width=10)
        searchButton = Button(root, text="Search", command=myClick, fg="white", bg="darkred")

        # Put widget onto the screen
        title.grid(row=0, column=1)
        description.grid(row=1, column=1)
        zipCode.grid(row=2, column=0)
        zipEntry.grid(row=2, column=1)
        searchButton.grid(row=2, column=2)

        # Create loop
        root.mainloop()
        
    def outputResults(self) -> None:
        """
        Prints results in terminal.
        """
        with open('tm-results.json', 'r') as infile:
            test_data = json.load(infile)
        for i in range(10):
            print(test_data["_embedded"]["events"][i]["name"] + " " + test_data["_embedded"]["events"][i]["dates"]["start"]["localDate"])

widg = gui()
widg.ui()
