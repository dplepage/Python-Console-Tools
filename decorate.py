import sys
import warnings

class MultipleMainWarning(Warning):
    pass

def main(fn):
    if fn.__module__ == '__main__':
        if hasattr(main,'_has_target'):
            warnings.warn(MultipleMainWarning("Too many mains!"))
        main._has_target=True
        import plac
        def call(fn, *args, **kwargs):
            try:
                plac.call(fn,*args,**kwargs)
            except Exception,e:
                print "{0}: {1}: {2}".format(sys.argv[0], type(e).__name__, e)
        call(fn)
