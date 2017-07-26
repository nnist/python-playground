from bs4 import BeautifulSoup
import urllib.request
import re

url = "https://duckduckgo.com/html?q=what%20is%20my%20ip"
page = urllib.request.urlopen(url)

print(page.getcode())
soup = BeautifulSoup(page, 'html.parser')

# Print page title
# titleTag = soup.html.head.title
# print(titleTag.string)

# Get contents
content = soup.find("div", { "class" : "zci__result" })

# Print first paragraph
# paragraph = content.find("p", {})

# Find all IP addresses on page
ips = re.findall(r'[0-9]+(?:\.[0-9]+){3}', content.get_text())
print(ips)
