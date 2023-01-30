import json
from tkinter import *

root = Tk()

def myClick():
    getZip = zipEntry.get()
    print(getZip)
    with open('tm-results.json', 'r') as infile:
        test_data = json.load(infile)
    for i in range(10):
        print(test_data["_embedded"]["events"][i]["name"] + " " + test_data["_embedded"]["events"][i]["dates"]["start"]["localDate"])
        # result = Label(root, )/

# Create widgets
title = Label(root, text="Hockey Finder")
description = Label(root, text="Find a hockey game near you: ")
zipCode = Label(root, text="Zip Code: ")
zipEntry = Entry(root, width=10)
searchButton = Button(root, text="Search", command=myClick, fg="white", bg="darkred")


# Puts widget onto the screen
title.grid(row=0, column=1)
description.grid(row=1, column=1)
zipCode.grid(row=2, column=0)
zipEntry.grid(row=2, column=1)
searchButton.grid(row=2, column=2)


# Create loop
root.mainloop()
