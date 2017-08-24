# TODO Load dictionary
# TODO Create list of TLDs
# TODO Find words ending with TLD (.de, .se) like co.de or comato.se

import string
from tqdm import *
import getopt
import sys
import itertools

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

    # Build list of tuples containing alphabet
    probs = ()
    for i in range(length):
        probs += (chars,)

    # Build list of domains
    domains = []
    for prob in itertools.product(*probs):
        domain = ''.join(prob) + tld
        domains.append(domain)

    print(domains)
    print("Checking %s domains..." % len(domains))

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print('Interrupted by user.')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
