# -*- coding: utf8 -*-

class decorator_without_arguments(object):

    def __init__(self, f):
        """
        If there are no decorator arguments, the function
        to be decorated is passed to the constructor.
        """
        print("Inside __init__()")
        self.f = f

    def __call__(self, *args):
        """
        The __call__ method is not called until the
        decorated function is called.
        """
        print("Inside __call__()")
        self.f(*args)
        print("After self.f(*args)")

@decorator_without_arguments
def sayHello(a1, a2, a3, a4):
    print('sayHello arguments:', a1, a2, a3, a4)

print("After decoration")

print("----------------Preparing to call sayHello()----------------")
sayHello("say", "hello", "argument", "list")
print("----------------After first sayHello() call----------------")
sayHello("a", "different", "set of", "arguments")
print("----------------After second sayHello() call----------------")

'''
Inside __init__()
After decoration
当 Python 解释器读取到 @decorator_without_arguments 时，由于 decorator_without_arguments 是装饰器，初始化需要被装饰的 f 做参数，
因此继续读取 def sayHello， 拿到参数后， 就执行 sayHello = decorator_without_arguments(sayHello), 是个 callable 对象。
以后 sayHello() 的调用就是 sayHello.__call__()
----------------Preparing to call sayHello()----------------
Inside __call__()
('sayHello arguments:', 'say', 'hello', 'argument', 'list')
After self.f(*args)
----------------After first sayHello() call----------------
Inside __call__()
('sayHello arguments:', 'a', 'different', 'set of', 'arguments')
After self.f(*args)
----------------After second sayHello() call----------------
'''