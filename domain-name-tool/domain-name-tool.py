# https://en.wikipedia.org/wiki/Domain_hack

import string
from tqdm import *
import getopt
import sys
import itertools
import urllib.request
from urllib.error import URLError, HTTPError

def check_domain(url):
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1; rv:37.0) Gecko/20100101 Firefox/37.0"
    try:
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req, timeout=2)
        html = response.read()
    except HTTPError as e:
        return e.code
    except URLError as e:
        return -2
        #print(str(e.reason))
    except:
        return 123
    else:
        return 200

def main(argv):
    length = 2
    tld = ".com"
    chars = "abcdefghijklmnopqrstuvwxyz"
    try:
        opts, args = getopt.getopt(argv,"hl:t:c:",["length=","tld=", "chars="])
    except getopt.GetoptError:
        print('usage: domain-checker.py -l <length> -t <tld> -c <chars>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('usage: domain-checker.py -l <length> -t <tld> -c <chars>')
            sys.exit()
        elif opt in ("-l", "--length"):
            length = int(arg)
        elif opt in ("-t", "--tld"):
            tld = str(arg)
        elif opt in ("-c", "--chars"):
            chars = str(arg)

    # Load dictionary, check for lines ending with tld
    domains = []
    with open('dictionary.txt') as f:
        for line in f:
            if(line[0:-1].endswith(tld)) and '-' not in line:
                domain = line[0:-(len(tld) + 1)] + "." + tld
                domains.append(domain)

    print("Checking %s domains..." % len(domains))

    for domain in domains:
        status = check_domain("http://" + domain)
        print("http://" + domain, "->", status)

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print('Interrupted by user.')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
