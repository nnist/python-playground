"""Scrape P2000 information from a website and store it in a database."""
# https://nl.wikipedia.org/wiki/P2000_(netwerk)

# TODO Scrape street + number from message details
# TODO Scrape city name from message details
# TODO Add http://p2000mobiel.nl scraper

import urllib.request
from urllib.error import URLError, HTTPError
import sys
import re
import sqlite3
import argparse
from multiprocessing.dummy import Pool
import os
from tqdm import tqdm
from bs4 import BeautifulSoup

def init_database():
    """Initialize the database."""
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

def insert_into_database(item):
    """Insert P2000 item into database."""
    conn = sqlite3.connect('data/p2000.db')
    cur = conn.cursor()

    # Check if message already exists
    result = cur.execute("""SELECT * FROM messages WHERE date_time=? \
                            AND type=? AND region=? AND details=?""",
                         (item['date_time'], item['calltype'], item['region'],
                          item['details']))
    results = result.fetchall()
    if not results:
        cur.execute("""INSERT INTO messages \
                       VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)""",
                    (item['date_time'], item['calltype'], item['region'],
                     item['priority'], item['postcode'],
                     item['details'], str(item['capcodes'])))
        conn.commit()
        cur.close()
        return True
    return False

class Scraper():
    """Scrape P2000 items from website and add them to the database."""
    def __init__(self, number_of_pages=1, offset=0, threads=1):
        self.number_of_pages = number_of_pages
        self.offset = offset
        self.threads = threads

    def scrape(self):
        """Scrape items from and add them to the database."""
        new_messages = 0
        print('Scraping', self.number_of_pages, 'pages...')

        # Build a list of urls to send to threads
        urls = []
        for i in range(self.number_of_pages):
            urls.append("http://www.p2000-online.net/p2000.php?Pagina=" +
                        str(i+self.offset) + "&AutoRefresh=uit")

        # Scrape pages using threads
        pool = Pool(self.threads)
        iterations = pool.imap_unordered(self.scrape_page, urls)
        pbar = tqdm(total=len(urls))
        for results in enumerate(iterations):
            pbar.update()
            for p2000_item in results[1]:
                if insert_into_database(p2000_item):
                    new_messages += 1

        # Close the bar and pool
        pbar.close()
        pool.close()
        pool.join()

        print('Done! Added', new_messages, 'new messages.')

    def scrape_page(self, url):
        """Scrape page for P2000 items and return them."""
        status = None
        html, status = self.get_page(url)
        table = None
        p2000_items = []

        if status == 200:
            soup = BeautifulSoup(html, 'html.parser')
            table = soup.find("table", {"style" : "align:center"})

        if table is None:
            status = 400
        else:
            # TODO Refactor
            status = 200
            p2000_item = {'date_time':None, 'calltype':None, 'region':None,
                          'priority':None, 'postcode':None, 'details':None,
                          'capcodes':[]}

            for row in table.findAll("tr"):
                cells = row.findAll("td")
                if len(cells) > 1:
                    date = cells[0].find(text=True)

                    if date is not None: # Regular message
                        if p2000_item['date_time'] is not None:
                            # Add item to list and clear it for next use
                            p2000_items.append(p2000_item)
                            p2000_item = {'date_time':None, 'calltype':None,
                                          'region':None, 'priority':None,
                                          'postcode':None, 'details':None,
                                          'capcodes':[]}

                        # Convert date and time to YYYY-MM-DD HH:MM:SS
                        time = cells[1].find(text=True)
                        date = '20' + date[6:8] + '-' + date[3:5] + \
                               '-' + date[0:2]
                        p2000_item['date_time'] = date + ' ' + time

                        p2000_item['calltype'] = cells[2].find(text=True)
                        p2000_item['region'] = cells[3].find(text=True)
                        p2000_item['details'] = cells[4].find(text=True)

                        # Find priority code in details (ex. A1, A 1, P 1)
                        re_results = re.findall(r'(PRIO|Prio|[ABP])\s*(\d)', \
                                                p2000_item['details'])
                        if re_results != []:
                            part1 = re_results[0][0]
                            part2 = re_results[0][1]
                            if part1 == 'PRIO' or part1 == 'Prio':
                                p2000_item['priority'] = 'P' + part2
                            else:
                                p2000_item['priority'] = str(part1) + str(part2)

                        # Find postcode (ex. 2356DF)
                        re_results = re.findall(r'\d{4}[A-Z]{2}',
                                                p2000_item['details'])
                        if re_results != []:
                            p2000_item['postcode'] = str(re_results[0])

                    else: # Capcode or empty
                        capcode_details = cells[4].find(text=True)
                        if capcode_details is not None: # Definitely a capcode
                            p2000_item['capcodes'] += [capcode_details]

        return p2000_items

    def get_page(self, url):
        """Get page and return it and the status code."""
        status = None
        html = None
        while status != 200: # TODO Do not retry indefinitely
            try:
                req = urllib.request.Request(url)#, headers=headers)
                response = urllib.request.urlopen(req, timeout=2)
                html = response.read()
            except HTTPError as ex:
                status = ex.code
            except URLError as ex:
                if str(ex.reason) == 'timed out':
                    status = 408
                else:
                    status = re.findall(r'[0-9]{3,}', str(ex.reason))
                    if status == []:
                        status = 520 # Unknown error
            except Exception as ex:
                if str(ex) == 'timed out':
                    status = 408
                else:
                    status = re.findall(r'[0-9]{3,}', str(ex))
                    if status == []:
                        status = 520 # Unknown error
            else:
                status = 200
        return html, status

def main(argv):
    """Scrape P2000 information from a website and store it in a database."""
    # ~415300 pages in total at Jun 5 2017
    parser = argparse.ArgumentParser(
        description="""Scrape P2000 information from a website and store it
                       in a database."""
    )
    parser.add_argument(
        '-p', '--pages', help="Number of pages to scrape", type=int, default=1
    )
    parser.add_argument(
        '-o', '--offset', help="Offset to start at", type=int, default=0
    )
    parser.add_argument(
        '-t', '--threads', help="Number of threads to use", type=int, default=1
    )
    args = parser.parse_args(argv)

    init_database()

    scraper = Scraper(args.pages, args.offset, args.threads)
    scraper.scrape()

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print('Interrupted by user.')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0) # pylint: disable=protected-access
