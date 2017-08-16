# TODO Length argument
# TODO Top level domain argument
# TODO Chars argument

from tqdm import *
import getopt
import sys

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hl:",["length="])
    except getopt.GetoptError:
        print('usage: domain-checker.py -l <length>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('usage: domain-checker.py -l <length>')
            sys.exit()
        elif opt in ("-l", "--length"):
            length = int(arg)

    # TODO Generate list of domains
    chars = list("abcdefghijklmnopqrstuvwxyz")

    domains = []

    # TODO Create a list of domains of length length
    # length = 1 -> [a-z] = 26
    # length = 3 -> [a-z][a-z][a-z] = 26 * 26 * 26

    # TODO Print total num of domains to check
    # print("Checking # domains...")

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print('Interrupted by user.')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
