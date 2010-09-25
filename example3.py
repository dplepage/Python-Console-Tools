import time
from decorate import main, showprogress, loop

@main
@showprogress
def foo():
    for i in loop(range(100)):
        time.sleep(.01)
    print "We're done!"
