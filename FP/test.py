# -*- coding: utf-8 -*-

def compare(a, b):
    return True if a > b else False

f = compare
print f(1,2)


def partition(low, high, l):
    temp = l[low]
    i = low
    j = high
    while (i < j):
        while (j > low and l[j] >= temp):
            j -= 1
        if i < j:    
            l[i] = l[j]
            i += 1
        while (i < high and l[i] <= temp):
            i += 1
        if i < j:
            l[j] = l[i]
            j -= 1
    l[i] = temp
    return i

def quck_sort(comparator, low, high, l):
    # 一定要加此限定
    if low < high:
        temp = l[low]
        i = low
        j = high
        while (i < j):
            while (j > low and l[j] >= temp):
                j -= 1
            if i < j:    
                l[i] = l[j]
                i += 1
            while (i < high and l[i] <= temp):
                i += 1
            if i < j:
                l[j] = l[i]
                j -= 1
        l[i] = temp

        print i, l[i]
        quck_sort(comparator, low, i-1, l)
        quck_sort(comparator, i+1, high, l)
    
    return l

l = [9,4,6,3,5,7]

print quck_sort(compare, 0, 5, l)



def fib(n):
    if n is 0 or n is 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

def trace_tree(f):
    f.indent = 0
    def wrapped(n):
        print '| ' * f.indent + '|--', f.__name__, n
        f.indent += 1
        value = f(n)
        print '| ' * f.indent + '|--', 'return', repr(value)
        f.indent -= 1
        return value
    return wrapped

def memoize(f):
    cache = {}
    def wrapped(n):
        if n not in cache:
            cache[n] = f(n)
        return cache[n]
    return wrapped


import time
def profile(f):
    def wrapped(n):
        start = time.time()
        value = f(n)
        end = time.time()
        print "time taken: %lf sec" % (end - start)
        return value
    return wrapped

print '-------------timing_trace_tree-----------'
fib = memoize(trace_tree(fib))
f = profile(fib)
print f(20)