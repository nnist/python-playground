import msvcrt
import time

print("Press 'escape' to quit...")

while 1:
    char = msvcrt.getwch()
    if char == chr(27):
        print("\nGoodbye!")
        time.sleep(2)
        break
    print(char, end="", flush=True)
    if char == chr(13):
        print()
