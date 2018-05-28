"""Print the ANSI escape codes for the base16 colors."""
from tabulate import tabulate

SELECTION = [1, 2, 3, 4, 7, 8] + list(range(30, 48)) + list(range(90, 108))
results = [('', '    ', 'normal', '████', '')]
results.append(('0', '    ', 'end', '', '\\033[0m'))
for i in SELECTION:
    results.append((i, '\033[%sm    \033[0m' % i,
                    '\033[%smexample\033[0m' % i,
                    '\033[%sm████\033[0m' % i,
                    '\033[%sm\\033[%sm\033[0m' % (i, i)))
print(tabulate(results))
