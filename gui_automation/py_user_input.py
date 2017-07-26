# https://github.com/PyUserInput/PyUserInput

from pymouse import PyMouse
from pykeyboard import PyKeyboard
import sys

m = PyMouse()
k = PyKeyboard()

# Click in the middle of the screen
# width, height = m.screen_size()
# m.click(int(width/2), int(height/2), 1)

# Alt-tab
# k.press_key(k.alt_key)
# k.tap_key(k.tab_key)
# k.release_key(k.alt_key)

# Type some text
# k.type_string('Hello, World!')

# Control keys
k.tap_key('a')

k.press_key('l')
k.release_key('l')

k.tap_key('l', n=2, interval=1) # Tap 'l' twice, 1 second interval
k.tap_key(k.function_keys[5]) # Tap F5
k.tap_key(k.numpad_keys['Home']) # Tap 'Home' on the numpad
k.tap_key(k.numpad_keys[5], n=3) # Tap 5 on the numpad, thrice

sys.exit()
