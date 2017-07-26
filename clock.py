import datetime
import msvcrt
import time
import sys

# def print_bars(num):
#     for i in range(0, num):
#         print("|", end="", flush=True)

print('Python version:')
print(sys.version)
print('')

CSI="\x1B["
reset=CSI+"m"
print(CSI+"31;40m" + "Colored Text" + CSI + "0m")

while 1:
    time.sleep(.01)
    currentTime = str(datetime.datetime.now().time())

    hours = int(currentTime[:2])
    minutes = int(currentTime[3:5])
    seconds = int(currentTime[6:8])

    # text = str(hours) + ":" + str(minutes) + ":" + str(seconds)
    text = currentTime[0:8]

    # print_bars(seconds)

    # print(text, end="\r", flush=True)

    # print(hours)
    # print(minutes)
    # print(seconds)
