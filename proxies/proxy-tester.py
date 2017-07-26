from bs4 import BeautifulSoup
from urllib.error import URLError, HTTPError
import urllib.request
import sys
import re
import sqlite3
import tqdm
import argparse
import logging
from multiprocessing.dummy import *
import os

# class TqdmLoggingHandler(logging.Handler):
    # def __init__(self, level = logging.NOTSET):
    #     super(self.__class__, self).__init__(level)
class TqdmLoggingHandler(logging.StreamHandler):
    def __init__(self):
        logging.StreamHandler.__init__(self)

    def emit(self, record):
        try:
            msg = self.format(record)
            tqdm.tqdm.write(msg)
            self.flush()
        except(KeyboardInterrupt, SystemExit):
            raise
        except:
            # self.handleError(record)
            pass # Might want to properly fix this..

def test_proxy(proxy):
    pkey = proxy[0]
    ip = proxy[1]
    port = proxy[2]

    log = logging.getLogger(__name__)
    log.debug('%s: Testing %s:%s', current_process().name, ip, port)

    test_url = "ipv4.icanhazip.com/"
    url_http = "http://" + test_url
    url_https = "https://" + test_url
    # TODO Optionally check for abuse history

    proxy_support = urllib.request.ProxyHandler({'http' : 'http://' + str(ip) + ':' + str(port),
                                                 'https': 'https://' + str(ip) + ':' + str(port)})
    opener = urllib.request.build_opener(proxy_support)
    urllib.request.install_opener(opener)

    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1; rv:37.0) Gecko/20100101 Firefox/37.0"

    proxy_type = 'unknown'
    status = 0

    # Test HTTP
    try:
        req = urllib.request.Request(url_http, headers=headers)
        response = urllib.request.urlopen(req, timeout=2)
        html = response.read()
    except HTTPError as e:
        status = e.code
    except URLError as e:
        if str(e.reason) == 'timed out':
            status = 408
        else:
            rx = re.findall(r'[0-9]{3,}', str(e.reason))
            if rx == []:
                status = 520 # Unknown error
            else:
                status = int(rx[0])
    except Exception as e:
        if str(e) == 'timed out':
            status = 408
        else:
            rx = re.findall(r'[0-9]{3,}', str(e))
            if rx == []:
                status = 520 # Unknown error
            else:
                status = int(rx[0])
    else:
        response_ip = re.findall(r"\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}", str(html))
        if len(response_ip) > 0:
            if response_ip[0] == ip:
                status = 200
                proxy_type = "http"

    log.debug('%s: %s:%s -> %s %s', current_process().name, ip, port, proxy_type, status)
    if status is 200:
        return pkey, proxy_type, status

    # Test HTTPS
    try:
        req = urllib.request.Request(url_https, headers=headers)
        response = urllib.request.urlopen(req, timeout=2)
        html = response.read()
    except HTTPError as e:
        status = e.code
    except URLError as e:
        if str(e.reason) == 'timed out':
            status = 408
        else:
            rx = re.findall(r'[0-9]{3,}', str(e.reason))
            if rx == []:
                status = 520 # Unknown error
            else:
                status = int(rx[0])
    except Exception as e:
        if str(e) == 'timed out':
            status = 408
        else:
            rx = re.findall(r'[0-9]{3,}', str(e))
            if rx == []:
                status = 520 # Unknown error
            else:
                status = int(rx[0])
    else:
        response_ip = re.findall(r"\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}", str(html))
        if len(response_ip) > 0:
            if response_ip[0] == ip:
                status = 200
                proxy_type = "https"

    log.debug('%s: %s:%s -> %s %s', current_process().name, ip, port, proxy_type, status)
    return pkey, proxy_type, status

def query_database(query):
    conn = sqlite3.connect('data/proxies.db')
    cur = conn.cursor()
    result = cur.execute(query)
    results = result.fetchall()
    cur.close()
    return results

def main(argv):
    threads = 1
    only_seen = False

    parser = argparse.ArgumentParser(description='Test proxies.')
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
        '-s', '--seen',
        help='Test only proxies that have been seen online',
        action='store_true'
    )
    parser.add_argument(
        '-t', '--threads',
        help='Number of threads to use',
        default=1
    )

    args = parser.parse_args()
    threads = int(args.threads)
    only_seen = bool(args.seen)

    log = logging.getLogger(__name__)
    log.setLevel(args.loglevel)
    handler = TqdmLoggingHandler()
    handler.setLevel(args.loglevel)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)

    if only_seen is True:
        proxies = query_database("""SELECT id, ip, port
                                    FROM proxies
                                    WHERE last_seen IS NOT NULL
                                """)
    else:
        proxies = query_database("""SELECT id, ip, port
                                    FROM proxies
                                """)

    working_proxies = []
    broken_proxies = []

    print('Testing', len(proxies), 'proxies...')
    pool = Pool(threads)
    it = pool.imap_unordered(test_proxy, proxies)
    pbar = tqdm.tqdm(total=len(proxies))
    for result in enumerate(it):
        pbar.update()
        proxy_type = result[1][1]
        proxy_pkey = result[1][0]
        proxy_status = result[1][2]
        if proxy_status is 200:
            working_proxies += [(proxy_type, proxy_status, proxy_pkey)]
        else:
            broken_proxies += [(proxy_status, proxy_pkey)]

    pbar.close()
    pool.close()
    pool.join()
    print('Done.')
    print('Working proxies:', len(working_proxies))
    print('Broken proxies:', len(broken_proxies))

    log.info('Updating database...')
    conn = sqlite3.connect('data/proxies.db')
    cur = conn.cursor()
    cur.executemany('''UPDATE proxies
                    SET last_seen = DATETIME('now', 'localtime'),
                    proxy_type = ?,
                    status = ?
                    WHERE id = ?''',
                    working_proxies)
    cur.executemany('''UPDATE proxies
                    SET status = ?
                    WHERE id = ?''',
                    broken_proxies)
    conn.commit()
    cur.close()
    log.info('Database updated.')

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
