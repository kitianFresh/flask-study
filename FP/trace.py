# -*- coding: utf-8 -*-

def fib(n):
    if n is 0 or n is 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

print 'fib', fib(3)

def fib_verbose(n):
    print fib_verbose.__name__, n
    if n is 0 or n is 1:
        print 'return', repr(1)
        return 1
    else:
        value = fib_verbose(n-1) + fib_verbose(n-2)
        print 'return', repr(value)
        return value
print '-------------fib_verbose-----------'
print fib_verbose(3)

indent = 0
def fib_verbose_tree(n):
    global indent 
    print '| ' * indent + '|--', 'fib', n
    indent += 1
    if n is 0 or n is 1:
        print '| ' * indent + '|--', 'return', repr(1)
        indent -= 1
        return 1
    else:
        value = fib_verbose_tree(n-1) + fib_verbose_tree(n-2)
        print '| ' * indent + '|--', 'return', repr(value)
        indent -= 1
        return value
print '-------------fib_verbose_tree-----------'
print fib_verbose_tree(4)

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

# print '-------------trace_tree-----------'
# fib = trace_tree(fib)
# print fib(4)


def memorize(f):
    cache = {}
    def wrapped(n):
        if n not in cache:
            cache[n] = f(n)
        return cache[n]
    return wrapped

print '-------------memorize_trace_tree-----------'
fib = trace_tree(fib)
fib = memorize(fib)
print fib(4)

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
fib = memorize(trace_tree(fib))
f = profile(fib)
print f(20)

# 对递归函数的装饰器，要特别小心，如果你要包装递归函数，并且想知道每一步递归的具体调用情况，
# 必须要让包装后的函数名和原来的递归函数名字一样，要不然被包装的递归函数只是在第一层包装了，
# 但是后面的每一层调用还是调用他原来的本尊（未加工的那个原始的函数）。这里只要知道函数式编程的本质是
# 函数是一等公民，可以像变量一样随时修改，赋值，还可以当参数和返回。例如 t = memorize(trace_tree(fib))
'''
t = memorize(trace_tree(fib))
print t(4)
|-- fib 4
| |-- return 5
5
打印的只有第一层的，但是确实算出来了最终结果，这说明fib一定完成了调用，但是trace_tree并没有，为什么？因为这里的trace_tree
并没有被改名为fib啊，所以在第一层的trace_tree打印之后，当递归进入下一层的时候，调用fib函数，可是fib函数是原来那个没有被装饰过的，
这就导致了看不到后面几层的调用过程了。如果你把先把trace_tree(fib)赋值给fib，然后再传递给memorize，就可以了，或者直接最终赋值fib
即 fib = trace_tree(fib) fib = memorize(fib)[如果这里改成f = memorize(fib) 呢？那结果就是可以trace，但是只有第一层会被缓存，即缓存失效了] 
或一步到位 fib = memorize(trace_tree(fib))

'''
def outer():
    count = 0
    def inner():
        # count += 1 #UnboundLocalError: local variable 'count' referenced before assignment
        return count
    return inner

counter = outer()
print counter()

def better_outer():
    count = [0]
    def inner():
        count[0] += 1
        return count[0]
    return inner

counter = better_outer()
print counter()