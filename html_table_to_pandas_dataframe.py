# http://www.generatedata.com/

import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

url = "file:///C:/Users/nnist/Documents/GitHub/python-playground/data_examples/name-birth-mail.html"
page = urllib.request.urlopen(url)
print(page)

soup = BeautifulSoup(page, "html.parser")

table = soup.find("table")
# print(table)

# Create empty lists
last_names = []
first_names = []
birthdates = []
emails = []

# Iterate through all rows in table
for row in table.findAll("tr"):
    # Find all cells in row
    cells = row.findAll("td")

    # Check if length of cells list is longer than 0 to ignore first entry
    if(len(cells) > 0):
        # Add cell contents to lists
        last_names.append(cells[0].find(text=True))
        first_names.append(cells[1].find(text=True))
        birthdates.append(cells[2].find(text=True))
        emails.append(cells[3].find(text=True))

# Create pandas dataframe, auto-ordered
# df = pd.DataFrame({ "Last name" : last_names,
#                     "First name" : first_names,
#                     "Birthdate" : birthdates,
#                     "E-mail" : emails})

# Create pandas dataframe, custom ordered
df = pd.DataFrame(last_names, columns=["Last name"])
df["First name"] = first_names
df["Birthdate"] = birthdates
df["E-mail"] = emails

print(df.to_string())

input("Press Enter to quit...")
