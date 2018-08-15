"""Print the ANSI escape codes for the base16 colors."""
# See https://en.wikipedia.org/wiki/ANSI_escape_code
# See https://misc.flogisoft.com/bash/tip_colors_and_formatting#terminals_compatibility
# This script is meant for xterm-256color but should work for most terms

from tabulate import tabulate

def create_line(i, text):
    text_tuple = (i, '\033[%sm    \033[0m' % i,
                  '\033[%smexample\033[0m' % i,
                  '\033[%sm████\033[0m' % i,
                  '\\033[%sm' % i, text)
    return text_tuple


names = ['normal', 'end', 'faint', 'italic', 'underline', 'slow blink',
         'rapid blink', 'reverse video', 'conceal', 'crossed-out'] # 0-9
names += [''] * 20
names += ['foreground color'] * 9 # 30-38
names += ['default foreground color'] # 39
names += ['background color'] * 9 # 40-48
names += ['default background color'] # 49
names += [''] # 50
names += ['framed', 'encircled', 'overlined'] # 51-53
names += [''] * 36
names += ['bright foreground color'] * 8 # 90-97
names += ['bright background color'] * 10 # 100-107

selection = list(range(0, 10)) + list(range(30, 50)) + list(range(51,54)) +\
            list(range(90, 98)) + list(range(100, 108))

results = []
for i in selection:
    results.append(create_line(i, names[i]))

headers = ('#', 'spaces', 'text', 'blocks', 'ANSI code', 'description')

print('\033[0m' + tabulate(results, headers=headers))
