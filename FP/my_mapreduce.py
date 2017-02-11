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
    def wrapper(*args):
        return "apple" + f(*args)
    return wrapper

def pineapple(f):
    def wrapper(*args):
        return "pineapple" + f(*args)
    return wrapper

def pen(f):
    def wrapper(*args):
        return "pen" + f(*args)
    return wrapper

def f1():
    return ''

a_pen = pen(f1)
print a_pen() + '\n'

an_apple = apple(f1)
print an_apple() + '\n'

apple_pen = apple(pen(f1))
print apple_pen() + '\n'

print a_pen() + '\n'
a_pineapple = pineapple(f1)
print a_pineapple() + '\n'
pineapple_pen = pineapple(pen(f1))
print pineapple_pen() + '\n'

print apple_pen() + '\n'
print pineapple_pen() + '\n'
ppap = pen(pineapple(apple(pen(f1))))
print ppap() + '\n'