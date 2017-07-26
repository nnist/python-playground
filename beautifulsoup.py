from bs4 import BeautifulSoup
import urllib.request
import sys
import re

def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)

url = "http://www.knmi.nl/nederland-nu/weer/verwachtingen"
page = urllib.request.urlopen(url)

soup = BeautifulSoup(page, 'html.parser')

# Print prettified HTML
# uprint(soup.prettify())

# Print all links on the page.
# for link in soup.find_all('a'):
#     print(link.get('href'))

# Print all text on the page.
# print(soup.get_text())

# result = soup.find_all(string=re.compile("view"))
# uprint(result)

# Print title
# titleTag = soup.html.head.title
# print(titleTag.string)

table = soup.find("ul", { "class" : "weather-map__table" })

for row in table.findAll("li"):
    cells = row.findAll("span")
    if len(cells) == 15:
        day = cells[0].find(text=True)
        print(day)
        # icon = cells[1].find(text=True)
        # print(icon)

        max_temp = cells[2].findAll(text=True)
        max_temp = re.findall(r'\d+', max_temp[2])
        print('Max:', max_temp)

        min_temp = cells[4].findAll(text=True)
        min_temp = re.findall(r'\d+', min_temp[2])
        print('Min:', min_temp)

        rain_amount = cells[6].findAll(text=True)
        rain_amount = re.findall(r'\d+', rain_amount[2])
        print('Rain amount:', rain_amount)

        rain_chance = cells[8].findAll(text=True)
        rain_chance = re.findall(r'\d+', rain_chance[2])
        print('Rain chance:', rain_chance)

        sun_chance = cells[10].findAll(text=True)
        sun_chance = re.findall(r'\d+', sun_chance[2])
        print('Sun chance:', sun_chance)

        wind = cells[12].findAll(text=True)
        # wind = wind[3].lstrip('\n').strip()
        wind_speed = re.findall(r'\d+', wind[3])
        wind_direction = re.findall(r'[A-Z]', wind[3])
        print('Wind speed:', wind_speed)
        print('Wind direction:', wind_direction)

        print(' ')

        if int(wind_speed[0]) > 3:
            print('wow much wind')
