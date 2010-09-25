import sys
from decorate import main

def fail(i):
    if i == 10:
        raise ValueError("Egad!")
    fail(i+1)

@main
def foo(name, n = 7, k = 11, pizza="delicious"):
    print ( "Running with name {name} and options n={n}, k={k}\n"
            "Also, pizza is {pizza}".format(**locals()))
    fail(1)

