import sys
import argparse
import random

def main(argv):
    parser = argparse.ArgumentParser(
        description="""Gets quick to type words from a dictionary."""
    )
    parser.add_argument(
    "--min", help="Minimum length of words",
    default=1, type=int
    )
    parser.add_argument(
    "--max", help="Maximum length of words",
    default=999, type=int
    )
    parser.add_argument(
    "-f", help="Dictionary file to use",
    dest="file", default="nederlands3.txt"
    )
    parser.add_argument(
    "-c", "--chars", help="Characters to allow",
    default="qwertiopasdfgjkl"
    )
    parser.add_argument(
    "-d", "--double", help="Allow double chars", action="store_true"
    )
    parser.add_argument(
    "-a", "--adjecent", help="Allow adjecent chars", action="store_true"
    )
    # TODO Add arg for number of words to return
    parser.add_argument(
    "-n", "--number", help="Number of words to return",
    default=0, type=int
    )
    args = parser.parse_args()
    length_min = args.min
    length_max = args.max
    double = bool(args.double)
    adjecent = bool(args.adjecent)
    dict_file = args.file
    allowed_chars = args.chars

    words = []
    with open(dict_file) as f:
        for line in f:
            word = line[0:-1].lower()
            prev_char = ""
            fail = False

            if len(word) >= length_min and len(word) <= length_max:
                #TODO disallow word if char is adjecent to prev_char
                for char in word:
                    if char not in allowed_chars:
                        fail = True
                        break
                    if double is False and prev_char == char:
                        fail = True
                        break
                    prev_char = char
                
                if fail is False:
                    words.append(word)

    result = ""
    if args.number != 0:
        for i in range(args.number):
            result += " " + random.choice(words)
    else:
        result = " ".join(words)
    print(result)

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print('Interrupted by user.')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
