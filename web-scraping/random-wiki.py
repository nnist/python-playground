from bs4 import BeautifulSoup
import urllib.request

url = "https://en.wikipedia.org/wiki/Special:Random"
page = urllib.request.urlopen(url)

soup = BeautifulSoup(page, 'html.parser')

# Print page title
titleTag = soup.html.head.title
print(titleTag.string)

# Get contents
content = soup.find("div", { "class" : "mw-content-ltr" })

# Print first paragraph
paragraph = content.find("p", {})
print(paragraph.get_text())
