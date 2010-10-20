import sys
import plac

from consolation import main

def fail(i):
    if i == 10: raise Exception("Egad!")
    fail(i+1)

def main(arg1):
    '''Print arg1'''
    print arg1
    fail(1)

def call(fn, *args, **kwargs):
    import plac
    try:
        plac.call(fn,*args,**kwargs)
    except Exception,e:
        print "{0}: {1}: {2}".format(sys.argv[0], type(e).__name__, e)

if __name__ == '__main__':
    call(main)