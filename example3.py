import time
import __builtin__
from functools import wraps
from progress_bar import progressinfo as pinf

def loop(x):
    return x

def showprogress(fn):
    @wraps(fn)
    def tmp(*args, **kw):
        global range
        x = range
        range = lambda *args, **kwargs: pinf(__builtins__.range(*args,**kwargs))
        fn(*args,**kw)
        range = x
    return tmp

# @showprogress

def doitalot():
    for i in loop(range(5)):
        print 'foo'
        # doabunchofstuff()

foobar = range(100)
@showprogress
def doabunchofstuff():
    '''
    >>> doabunchofstuff()
    Done!
    '''
    for i in foobar:
        time.sleep(.01)
    print "Done!"

doabunchofstuff()

# import doctest
# doctest.testmod()