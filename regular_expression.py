# http://pythex.org/

import re

def checkBirthYear(year):
    m = re.search("^(19|20)\d{2}$", year)

    if m:
        if (int(year) < 2017):
            return True
    return False

if checkBirthYear("1900"):
    print("ye")
else:
    print("nah")
