# https://nl.wikipedia.org/wiki/P2000_(netwerk)

# This script scrapes P2000 information from a website and stores it in a database.

# TODO Scrape street + number from message details
# TODO Scrape city name from message details

from bs4 import BeautifulSoup
import urllib.request
from urllib.error import URLError, HTTPError
import sys
import re
import sqlite3
from tqdm import *
import getopt
from multiprocessing.dummy import Pool
import os

def init_database():
    conn = sqlite3.connect('data/p2000.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY,
        date_time DATETIME NOT NULL,
        type VARCHAR,
        region VARCHAR,
        priority VARCHAR,
        postcode VARCHAR,
        details VARCHAR,
        capcodes VARCHAR
    )""")
    conn.commit()
    cur.close()

def insert_into_database(date_time, calltype, region, priority, postcode, details, capcodes):
    conn = sqlite3.connect('data/p2000.db')
    cur = conn.cursor()

    # Check if message already exists
    result = cur.execute("""SELECT * FROM messages WHERE date_time=? AND type=? AND region=? AND details=?""",
    (date_time, calltype, region, details))
    results = result.fetchall()
    if(not results):
        cur.execute("""INSERT INTO messages VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)""",
        (date_time, calltype, region, priority, postcode, details, capcodes))
        conn.commit()
        cur.close()
        return True
    return False

def get_proxy():
    conn = sqlite3.connect('data/proxies.db')
    cur = conn.cursor()
    result = cur.execute("""SELECT ip, port, proxy_type, status, last_seen
                                FROM proxies
                                WHERE last_seen IS NOT NULL AND status IS 200 AND proxy_type IS 'http'
                                ORDER BY RANDOM()
                                LIMIT 1
                            """)
    results = result.fetchall()
    cur.close()
    proxy = str(results[0][0]) + ":" + str(results[0][1])
    return proxy

def get_page_using_proxy(url):
    status = None
    html = None
    while status is not 200:
        proxy = get_proxy()
        proxy_support = urllib.request.ProxyHandler({'http' : 'http://' + proxy,
                                                     'https': 'https://' + proxy})
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)

        try:
            req = urllib.request.Request(url)#, headers=headers)
            response = urllib.request.urlopen(req, timeout=2)
            html = response.read()
        except HTTPError as e:
            status = e.code
        except URLError as e:
            if str(e.reason) == 'timed out':
                status = 408
            else:
                status = re.findall(r'[0-9]{3,}', str(e.reason))
                if status == []:
                    status = 520 # Unknown error
        except Exception as e:
            if str(e) == 'timed out':
                status = 408
            else:
                status = re.findall(r'[0-9]{3,}', str(e))
                if status == []:
                    status = 520 # Unknown error
        else:
            status = 200
    return html, status

def scrape_page(url):
    status = None
    new_messages = 0
    html, status = get_page_using_proxy(url)
    table = None

    if status is 200:
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find("table", { "style" : "align:center" })

    if table is None:
        status = 400
    else:
        status = 200
        date_time = None
        calltype = None
        region = None
        priority = None
        postcode = None
        details = None
        capcodes = []

        for row in table.findAll("tr"):
            cells = row.findAll("td")
            if(len(cells) > 1):
                date = cells[0].find(text=True)

                if(date is not None): # Regular message
                    if(date_time is not None):
                        if insert_into_database(date_time, calltype, region, priority, postcode, details, str(capcodes)):
                            new_messages += 1
                        # Clear all variables
                        date_time = None
                        calltype = None
                        region = None
                        priority = None
                        postcode = None
                        details = None
                        capcodes = []

                    # Convert date and time to YYYY-MM-DD HH:MM:SS
                    time = cells[1].find(text=True)
                    date = '20' + date[6:8] + '-' + date[3:5] + '-' + date[0:2]
                    date_time = date + ' ' + time

                    calltype = cells[2].find(text=True)
                    region = cells[3].find(text=True)
                    details = cells[4].find(text=True)

                    # Find priority code in details (ex. A1, A 1, P 1)
                    re_results = re.findall(r'(PRIO|Prio|[ABP])\s*(\d)', details)
                    if(len(re_results) > 0):
                        a = re_results[0][0]
                        b = re_results[0][1]
                        if(a == 'PRIO' or a == 'Prio'):
                            priority = 'P' + b
                        else:
                            priority = str(a) + str(b)
                    # Find postcode (ex. 2356DF)
                    re_results = re.findall(r'\d{4}[A-Z]{2}', details)
                    if(re_results != []):
                        postcode = str(re_results[0])
                else: # Capcode or empty
                    capcode_details = cells[4].find(text=True)
                    if(capcode_details is not None): # Definitely a capcode
                        capcodes += [capcode_details]
    return new_messages

def main(argv):
    # ~415300 pages in total at Jun 5 2017
    number_of_pages = 1
    offset = 0
    threads = 1

    try:
        opts, args = getopt.getopt(argv,"hp:o:t:",["pages=", "offset=", "threads="])
    except getopt.GetoptError:
        print('usage: p2000.py -p <pages> -o <offset> -t <threads>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('usage: p2000.py -p <pages> -o <offset> -t <threads>')
            sys.exit()
        elif opt in ("-p", "--pages"):
            number_of_pages = int(arg)
        elif opt in ("-o", "--offset"):
            offset = int(arg)
        elif opt in ("-t", "--threads"):
            threads = int(arg)

    new_messages = 0

    print('Scraping', number_of_pages, 'pages...')
    init_database()

    # Build a list of urls to send to threads
    urls = []
    for i in range(number_of_pages):
        urls.append("http://www.p2000-online.net/p2000.php?Pagina=" + str(i+offset) + "&AutoRefresh=uit")

    # Scrape pages using threads
    pool = Pool(threads)
    it = pool.imap_unordered(scrape_page, urls)
    pbar = tqdm(total=len(urls))
    for result in enumerate(it):
        pbar.update()
        new_messages += result[1]

    # Close the bar and pool
    pbar.close()
    pool.close()
    pool.join()

    print('Done! Added', new_messages, 'new messages.')

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print('Interrupted by user.')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
