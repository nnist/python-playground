#!/usr/bin/env python

import curses
import curses.textpad
import time
import os, sys

def main(argv):
    stdscr = curses.initscr()
    curses.noecho()
    begin_x = 20
    begin_y = 7
    height = 5
    width = 40
    win = curses.newwin(height, width, begin_y, begin_x)
    #curses.echo() # Used for text editing etc
    #tb = curses.textpad.Textbox(win)
    #text = tb.edit()
    #curses.addstr(4,1,text.encode('utf_8'))
    
    hw = "Hello world!"
    while 1:
        c = stdscr.getch()
        if c == ord('p'): 
            print('p was pressed')
        elif c == ord('q'):
            break
        elif c == curses.KEY_HOME:
            x = y = 0
    
    curses.nocbreak()
    curses.echo()
    curses.endwin()
    sys.exit(0)

if __name__ == "__main__":
    try:
        curses.wrapper(main(sys.argv[1:]))
    except KeyboardInterrupt:
        try:
            curses.nocbreak()
            curses.echo()
            curses.endwin()
            sys.exit(0)
        except SystemExit:
            os._exit(0)
