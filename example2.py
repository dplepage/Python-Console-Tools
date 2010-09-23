from decorate import subcommand, run_subcommands

@subcommand
def cmd1():
    print "hi!"

@subcommand
def cmd2(arg="arg!"):
    print "Called cmd2 with arg: {0}",format(arg)

if __name__ == '__main__':
    run_subcommands()
