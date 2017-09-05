from inspect import getcallargs

def fun():
    print "subcriber__init__"


def authenticate(request=None, **credentials):
    """
    If the given credentials are valid, return a User object.
    """
    print request, credentials

pos = (1,2)
named = {'a': 1}


def f(a, *pos, **named):
    print a


