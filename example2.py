'''help for this module'''
from decorate import subcommand, run_subcommands

@subcommand
def cmd1():
    print "hi!"

@subcommand
def cmd2(arg="arg!"):
    '''
    Do useful stuff
    
    >>> cmd2('foo')
    Called cmd2 with arg: foo
    '''
    print "Called cmd2 with arg: {0}".format(arg)

if __name__ == '__main__':
    run_subcommands()
