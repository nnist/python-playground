# https://en.wikipedia.org/wiki/Domain_hack

import whois
import string
import getopt
import sys
import itertools
import urllib.request
from urllib.error import URLError, HTTPError

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
            line = line[0:-1].lower()
            if(line.endswith(tld)) and '-' not in line:
                if(len(line) <= length):
                    domain = line[0:-(len(tld))] + "." + tld
                    domains.append(domain)

    print("Checking %s domains..." % len(domains))

    for i in range(len(domains)):
        print("[" + str(i) + "/" + str(len(domains)) + "] " + domains[i], end=" -> ", flush=True)
        try:
            w = whois.whois(domains[i])
        except:
            print("whois error")
        else:
            if(all(x==None for x in w.values())):
                print("whois empty")
            else:
                print("whois not empty")

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print('Interrupted by user.')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
