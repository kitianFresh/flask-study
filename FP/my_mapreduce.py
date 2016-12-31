# -*- coding: utf-8 -*-

def my_map(operation, sequence):
    result = []
    for s in sequence:
        if isinstance(s, list):
            result.append(my_map(operation, s))
        else:
            result.append(operation(s))
    return result

l = [1,2,3,4,5,6]
n_l = [1,2,[3,4,[5,6]]]
print my_map(lambda x: x*x, l)
print my_map(lambda x: x*x, n_l)

print map(lambda x: x*x , l)
# print map(lambda x: x*x, n_l) #TypeError: can't multiply sequence by non-int of type 'list'




def apple(f):
    def wrapped(*args):
        return "apple" + f(*args)
    return wrapped

def pineapple(f):
    def wrapped(*args):
        return "pineapple" + f(*args)
    return wrapped


@apple
def pen():
    return 'pen'

print pen()

