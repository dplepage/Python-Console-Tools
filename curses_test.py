from __future__ import division
import curses
from contextlib import contextmanager
import time

@contextmanager
def curseswin():
    try:
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(1)
        yield stdscr
    finally:
        curses.nocbreak();
        stdscr.keypad(0);
        curses.echo()
        curses.endwin()

if __name__ == '__main__':
    with curseswin() as scr:
        for i in range(100):
            p = ["["]+["=" if x/50 < i/100 else '-' for x in range(50)]+["]"]
            scr.addstr(5,5, ''.join(p))
            scr.refresh()
            time.sleep(.01)
