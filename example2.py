import plac

subs = []
def subcommand(fn):
    subs.append(fn)
    return fn

@subcommand
def cmd1():
    print "hi!"

@subcommand
def cmd2():
    print "ho!"


class Foo(object):
    commands = [f.__name__ for f in subs]
    def _dummy(): pass
    
for cmd in subs:
    setattr(Foo, cmd.__name__, lambda self, *args, **kwargs: globals()[cmd.__name__](*args,**kwargs))
    
if __name__ == '__main__':
    plac.Interpreter.call(Foo)