import sys
import warnings
import plac

class MultipleMainWarning(Warning):
    pass

def main(fn):
    if fn.__module__ == '__main__':
        if hasattr(main,'_has_target'):
            warnings.warn(MultipleMainWarning("Too many mains!"))
        main._has_target=True
        def call(fn, *args, **kwargs):
            try:
                plac.call(fn,*args,**kwargs)
            except Exception,e:
                print "{0}: {1}: {2}".format(sys.argv[0], type(e).__name__, e)
        call(fn)


subs = []
def subcommand(fn):
    subs.append(fn)
    return fn

def run_subcommands():
    class Foo(object):
        commands = [f.__name__ for f in subs]
        def _dummy(): pass
    
    for cmd in subs:
        setattr(Foo, cmd.__name__, staticmethod(cmd))
    plac.Interpreter.call(Foo)
