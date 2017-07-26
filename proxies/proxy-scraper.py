from bs4 import BeautifulSoup
from urllib.error import URLError, HTTPError
import urllib.request
import sys
import re
import sqlite3
import logging
import tqdm
from multiprocessing.dummy import Pool as Pool_threads
from multiprocessing import Pool
import os
import argparse

class TqdmLoggingHandler(logging.Handler):
    def __init__(self, level = logging.NOTSET):
        super(self.__class__, self).__init__(level)

    def emit(self, record):
        try:
            msg = self.format(record)
            tqdm.tqdm.write(msg)
            self.flush()
        except(KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

def init_database():
    conn = sqlite3.connect('data/proxies.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS proxies (
        id INTEGER PRIMARY KEY,
        ip VARCHAR UNIQUE,
        port INT,
        last_seen DATETIME,
        proxy_type VARCHAR,
        status INT
    )""")
    conn.commit()
    cur.close()

def scrape_google(pages=1, offset=0):
    # Searches for proxy lists using Google dorks
    # Returns list of file URLs
    log = logging.getLogger(__name__)
    file_urls = []
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1; rv:37.0) Gecko/20100101 Firefox/37.0"

    # proxy = '128.199.138.78:8080'
    # proxy_support = urllib.request.ProxyHandler({'http' : 'http://' + proxy,
    #                                              'https': 'https://' + proxy})
    # opener = urllib.request.build_opener(proxy_support)
    # urllib.request.install_opener(opener)

    current_url = """https://www.google.com/search?q=\":8080\"++\":3128\"++\":80\"+filetype:txt&filter=0&start=""" + str(offset*10)

    pbar = tqdm.tqdm(total=pages)
    for i in range(pages):
        try:
            req = urllib.request.Request(current_url, headers=headers)
            response = urllib.request.urlopen(req, timeout=2)
            html = response.read()
        except HTTPError as e:
            code = e.code
            if(code == 503):
                pbar.close()
                log.error('Google returned 503 error, giving up')
                return file_urls
            else:
                log.warning('%s HTTPError: %s', current_url, str(code))
        except URLError as e:
            log.warning('%s URLError: %s', current_url, str(e.reason))
        except Exception as e:
            log.warning('%s Exception: %s', current_url, str(e))
        else:
            soup = BeautifulSoup(html, 'html.parser')
            # TODO Traverse through page instead of using find function, should be a lot faster
            for link in soup.find_all('a'):
                url = str(link.get('href'))
                if(url.endswith('.txt')):
                    file_urls.append(url)

            button = soup.find('a', id='pnnext')

            if button is not None:
                button_url = button.get('href')
                current_url = 'https://www.google.de' + button_url
            else: # Last result page does not have 'next' button
                pbar.close()
                log.info('Last Google page reached')
                return file_urls
        pbar.update()

    pbar.close()
    return file_urls

def scrape_text_file_worker(file_url):
    # Scrapes a text file for proxies, returns a list
    log = logging.getLogger(__name__)
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1; rv:37.0) Gecko/20100101 Firefox/37.0"
    log.debug('Scraping %s', file_url)
    try:
        req = urllib.request.Request(file_url, headers=headers)
        response = urllib.request.urlopen(req, timeout=2)
        html = response.read()
    except:
        return []
    else:
        # Find all proxies with format ip:port
        proxies = re.findall(r"\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}\s*?[:]\s*?\d{1,5}", str(html))
        return proxies

def scrape_text_files(file_urls, threads=1):
    # Returns big list of proxies
    log = logging.getLogger(__name__)
    proxies = []

    pool = Pool_threads(threads)
    it = pool.imap_unordered(scrape_text_file_worker, file_urls)
    pbar = tqdm.tqdm(total=len(file_urls))
    for results in enumerate(it):
        pbar.update()
        for result in results[1]:
            proxies.append(result)

    pbar.close()
    pool.close()
    pool.join()
    return proxies

def scrape_url_worker(url):
    """
    Attempts to scrape IPs and their ports from url.
    Returns list of tuples, which contain IPs and ports.
    """
    log = logging.getLogger(__name__)
    log.debug('Scraping %s', url)
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1; rv:37.0) Gecko/20100101 Firefox/37.0"

    try:
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req, timeout=2)
        html = response.read()
    except HTTPError as e:
        log.warning('%s HTTPError: %s', url, str(e.code))
        return []
    except URLError as e:
        log.warning('%s URLError: %s', url, str(e.reason))
        return []
    except Exception as e:
        log.warning('%s Exception: %s', url, str(e))
        return []
    else:
        soup = BeautifulSoup(html, 'html.parser')

        # Finds all ip:port combinations, this does not need further processing
        proxies = soup.find_all(text=re.compile(r"(\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3})\s*?[:]\s*?(\d{1,5})"))
        if(len(proxies) > 1):
            proxies_split = []
            for proxy in proxies:
                ip = proxy.split(':')[0]
                port = proxy.split(':')[1]
                proxies_split.append((ip, port))
            return proxies_split

        # Finds all IPs
        ips = soup.find_all(text=re.compile(r"(\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3})"))

        if len(ips) <= 1: # Site shows no IPs, or only our own.
            return []

        # Traverse up, find the table we're in
        table = ips[1].parent.parent.parent

        # Extract all IPs and ports from table
        rows = table.find_all('tr')
        proxies = []
        for row in rows:
            proxy = re.findall(r"(\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}).*?(\d{2,5})", str(row))
            proxy_type = re.findall(r"(http[s]?|socks[45])", str(row))
            proxies.append((proxy[0][0], proxy[0][1]))

        return proxies

def main(argv):
    number_of_pages = 1
    offset = 0
    threads = 1
    google = False
    free = False
    proxies_tuples = []

    parser = argparse.ArgumentParser(description='Scrape proxies from the web.')
    parser.add_argument(
        '-d', '--debug',
        help="Print lots of debugging statements",
        action="store_const", dest="loglevel", const=logging.DEBUG,
        default=logging.ERROR,
    )
    parser.add_argument(
        '-v', '--verbose',
        help='Be verbose',
        action='store_const', dest='loglevel', const=logging.INFO,
        default=logging.ERROR,
    )
    parser.add_argument(
        '-f', '--free',
        help='Scrape free proxy sources',
        action='store_true'
    )
    parser.add_argument(
        '-g', '--google',
        help='Scrape Google for proxylists',
        action='store_true'
    )
    parser.add_argument(
        '-p', '--pages',
        help='Number of Google pages to scrape',
        default=1
    )
    parser.add_argument(
        '-o', '--offset',
        help='Offset for Google scraping',
        default=0
    )
    parser.add_argument(
        '-t', '--threads',
        help='Number of threads to use',
        default=1
    )

    args = parser.parse_args()
    number_of_pages = int(args.pages)
    offset = int(args.offset)
    threads = int(args.threads)
    free = bool(args.free)
    google = bool(args.google)

    log = logging.getLogger(__name__)
    log.setLevel(args.loglevel)
    handler = TqdmLoggingHandler()
    handler.setLevel(args.loglevel)
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)

    init_database()

    # Scrape Google for proxy lists
    if google is True:
        if offset is 0:
            print('Scraping', number_of_pages, 'Google pages...')
        else:
            print('Scraping', number_of_pages, 'Google pages... (starting at page', str(offset) + ')')

        # Retrieve a list of file urls
        file_urls = scrape_google(number_of_pages, offset)
        print('Retrieved', len(file_urls), 'file urls')

        # Scrape file urls for proxies
        print('Scraping proxies in', len(file_urls), 'urls')
        proxies = scrape_text_files(file_urls, threads)
        print('Retrieved', len(proxies), 'proxies')

        # Split all proxies into ip and port
        for proxy in proxies:
            ip = proxy.split(':')[0]
            port = proxy.split(':')[1]
            proxies_tuples.append((ip, port))

    # Scrape free proxylists
    if free is True:
        urls = ['https://www.proxynova.com/proxy-server-list/country-ua/',
        'https://www.free-proxy-list.net/',
        'https://www.us-proxy.org/',
        'https://hidester.com/proxylist/',
        'http://www.proxylist.ro/',
        'https://www.sslproxies.org/#list',
        ]

        # Build URLs
        for i in range(5):
            urls.append('http://www.proxylist.ro/large-proxy-list-http-' + str(i) + '.html')

        for i in range(9):
            urls.append('https://proxy-list.org/english/index.php?p=' + str(i+1))

        for i in range(50):
            urls.append('http://freeproxylists.net/?page=' + str(i+1))

        # Scrape proxies from list of URLs
        print('Scraping', str(len(urls)), 'pages...')
        proxies_retrieved = 0
        pool = Pool_threads(threads)
        it = pool.imap_unordered(scrape_url_worker, urls)
        pbar = tqdm.tqdm(total=len(urls))
        for results in enumerate(it):
            pbar.update()
            proxies = results[1]
            proxies_retrieved += len(proxies)
            for proxy in proxies:
                proxies_tuples.append(proxy)

        pbar.close()
        pool.close()
        pool.join()
        print('Retrieved', str(proxies_retrieved), 'proxies')

    # Put proxies into database
    conn = sqlite3.connect('data/proxies.db')
    cur = conn.cursor()
    derp = cur.executemany('''INSERT OR IGNORE INTO proxies VALUES (NULL, ?, ?, NULL, NULL, NULL)''', proxies_tuples)
    conn.commit()
    cur.close()

    print('Done.')
    sys.exit(0)

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print('Interrupted by user.')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
