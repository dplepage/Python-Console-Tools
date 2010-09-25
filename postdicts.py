import time
import sys

class RedrawDict(dict):
    def __setitem__(self, key, item):
        super(RedrawDict, self).__setitem__(key, item)
        sys.stdout.write('\r'+`self`)
        sys.stdout.flush()

def redraw_dict(fn):
    def new(*args,**kwargs):
        x = __builtins__.dict
        __builtins__.dict = RedrawDict
        fn(*args, **kwargs)
        __builtins__.dict = x
    return new

updating_dicts = set()

@draw
def do_stuff():
    d = dict()
    draw_set.add(d)
    for i in range(10):
        time.sleep(1)
        d['foo'] = i
        # d2['bar'] = i
    
do_stuff()