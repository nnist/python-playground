import sys

progress = 0
while progress < 100:
    sys.stdout.write('\r[%s%s]' % ('=' * progress, ' ' * (50 - progress)))
    sys.stdout.flush()
    progress += 1
