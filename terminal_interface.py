'''
This is a terminal GUI to interface with
all of the things this project may need.
This includes:
 -Viewing current stock
 -Running and terminating automatic trading
 -Making manual trades
'''
import curses

# Prepping terminal
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)

# Closing curses and reverting terminal
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()
