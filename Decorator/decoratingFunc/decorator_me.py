# -*- coding: utf-8 -*-

# Python 规定 decorator 返回的对象必须是 callable 的， 因此使用类定义的 decorator 必须实现 __call__() 方法
class decorator_me(object):

    def __init__(self, f):
        print("inside decorator_me.__init__()")
        f()

    def __call__(self):
        print ("inside decorator_me.__call__()")

@decorator_me
def aFunction():
    print("inside aFunction")

print("Finished decorating aFunction")

aFunction()

'''
inside decorator_me.__init__()
inside aFunction
Finished decorating aFunction
inside decorator_me.__call__()
从输出可以看出，Python 解释器在解释到@decorator_me的时候，就会进行装饰，这个装饰过程，
说白了，就是把 aFunction 变成了 decorator_me(aFunction)对象,然后继续解释执行，当遇到 aFunction
的时候，就是调用 decorator_me.__call__() 了。

'''
