import json
from tkinter import *

root = Tk()

def myClick():
    myLabel = Label(root, text="The games are in the command line which is dumb")
    myLabel.grid(row=2, column=0)
    with open('tm-results.json', 'r') as infile:
        test_data = json.load(infile)
    for i in range(10):
        print(test_data["_embedded"]["events"][i]["name"] + " " + test_data["_embedded"]["events"][i]["dates"]["start"]["localDate"])
        

# Create widgets
myLabel1 = Label(root, text="Hockey Finder")
myLabel2 = Label(root, text="Zip Code: ")
myButton = Button(root, text="Search", padx=5, command=myClick)

# Puts it onto the screen
myLabel1.grid(row=0, column=0)
myLabel2.grid(row=1, column=0)
myButton.grid(row=1, column=1)


# Create loop
root.mainloop()
