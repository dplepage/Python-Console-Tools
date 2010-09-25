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

@redraw_dict
def do_progress():
    d = dict(x=12, foo=19)
    for i in range(10):
        time.sleep(1)
        d['foo'] = i
    print

do_progress()


def main():
    info.draw("dictx", 'loop2')