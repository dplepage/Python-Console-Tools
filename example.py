import sys
from decorate import main

def fail(i):
    if i == 10:
        raise ValueError("Egad!")
    fail(i+1)


@main
def foo(set_name, k=3, patch_size=7, w_err=.1, w_sm=.2):
    print ( "Running on set {set_name} with options K={k}, "
            "patch_size={patch_size} w_err={w_err}, w_sm={w_sm}".format(**locals()))
    fail(1)


# foo('foo')
# @main
# def bar(*args):
#     print args