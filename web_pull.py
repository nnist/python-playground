# https://docs.python.org/2/library/urllib.html

import urllib.request

print("Enter URL:")

valid = False

while valid == False:
    # url = input('> ')
    url = "https://wtfismyip.com/"
    #url = "http://www.ictlab.nl"
    try:
        page = urllib.request.urlopen(url)
        break
    except:
        print("Invalid URL. Try again.")

print("\nStatus code:")
print(page.getcode())
print("\nHeader:")
print(page.info())
print("Contents:")
print(page.read())

input("\nPress Enter to close...")
