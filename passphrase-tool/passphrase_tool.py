import sys
import argparse
import random

class PassphraseGenerator:
    """Generate passphrase words."""
    def __init__(self, length_min=1, length_max=999, double=False,
                 adjecent=False, allowed_chars="qwertiopasdfgjkl",
                 dict_file="nederlands3.txt", number=3):
        self.dict_file = dict_file
        self.length_min = length_min
        self.length_max = length_max
        self.allowed_chars = allowed_chars
        self.double = double
        self.number = number

    def generate(self):
        """Open the dictionary file and return a list of words that
           meet the requirements."""
        words = []
        with open(self.dict_file) as f:
            for line in f:
                word = line[0:-1].lower()
                prev_char = ""
                fail = False

                if len(word) >= self.length_min and \
                   len(word) <= self.length_max:
                    #TODO disallow word if char is adjecent to prev_char
                    for char in word:
                        if char not in self.allowed_chars:
                            fail = True
                            break
                        if self.double is False and prev_char == char:
                            fail = True
                            break
                        prev_char = char

                    if fail is False:
                        words.append(word)

        selected_words = []
        if self.number != 0:
            for i in range(self.number):
                selected_words.append(random.choice(words))
        else:
            selected_words = words
        return selected_words

def main(argv):
    """Generate words for use in passphrases and print them to stdout."""
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
    number = args.number

    generator = PassphraseGenerator(length_min, length_max, double, adjecent,
                                    allowed_chars, dict_file, number)
    result = generator.generate()
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
