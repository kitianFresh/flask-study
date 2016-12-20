# -*- coding: utf8 -*-

class counter(object):

    def __init__(self, name, count=0):
        self.count = count
        self.name = name

    def __call__(self, f):
        def wrapped(*args):
            f(*args)
            self.count += 1
            print("Decorator %s records that function %s has been called %d times" % (self.name, f.__name__, self.count))
        return wrapped

@counter("sayByeCounter")
def sayBye(who):
    print("good bye %s" % (who))

sayBye("Kinny")
sayBye("Sweetie")
sayBye("World")