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



import time

def timing(f):
    '''
    Outputs the time a function takes to execute
    '''
    def wrapped():
        start = time.time()
        f()
        end = time.time()
        return "Time it took to run the function %s : %d\n" %(f.__name__, end-start)
    return wrapped
@timing
def tick():
    num_list = []
    for num in (range(0, 100000000)):
        num_list.append(num)
    print("sum: %d"%(sum(num_list)))

print(tick())

