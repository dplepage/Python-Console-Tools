import time
from decorate import main
from functools import wraps
import sys
from progress_bar import progressinfo as pinf

def loop(x):
    return x

def showprogress(fn):
    @wraps(fn)
    def tmp(*args, **kw):
        global loop
        x = loop
        loop = lambda a: pinf(x(a))
        fn(*args,**kw)
        loop = x
    return tmp
import time

@main
@showprogress
def foo():
    for i in loop(range(100)):
        time.sleep(.01)
    print "We're done!"
