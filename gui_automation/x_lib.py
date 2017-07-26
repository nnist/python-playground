from Xlib import X, display

d = display.Display()
s = d.screen()
root = s.root
root.warp_pointer(300,300)
d.sync()

Xlib.ext.xtest.fake_input(d, X.ButtonPress, 1)
d.sync()
time.sleep(0.001)
Xlib.ext.xtest.fake_input(d, X.ButtonRelease, 1)
d.sync()
