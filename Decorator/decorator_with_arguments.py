# -*- coding: utf8 -*-

class decorator_with_arguments(object):

    def __init__(self, arg1, arg2, arg3):
        """
        If there are decorator arguments, the function
        to be decorated is not passed to the constructor!
        """
        print("Inside __init__()")
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3

    def __call__(self, f):
        """
        If there are decorator arguments, __call__() is only called
        once, as part of the decoration process! You can only give
        it a single argument, which is the function object.
        """
        print("Inside __call__()")
        def wrapped_f(*args):
            print("Inside wrapped_f()")
            print("Decorator arguments:", self.arg1, self.arg2, self.arg3)
            f(*args)
            print("After f(*args)")
        return wrapped_f

@decorator_with_arguments("hello", "world", 22)
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
Inside __call__()
当 Python 解释器读取到 @decorator_with_arguments("hello", "world", 22) 时完成初始化，带参数的 decorator 首先使用其参数初始化，
dwa = decorator_with_arguments("hello", "world", 22)。由于 decorator_with_arguments 是装饰器，需要被装饰的 f 做参数，
因此继续读取 def sayHello， 拿到参数后， 就执行 sayHello = dwa(sayHello), 返回的是 wrapped_f。class decorator的 解释模型 就是
f = dcwa(args)(f) => f()

After decoration
----------------Preparing to call sayHello()----------------
Inside wrapped_f()
('Decorator arguments:', 'hello', 'world', 22)
('sayHello arguments:', 'say', 'hello', 'argument', 'list')
After f(*args)
----------------After first sayHello() call----------------
Inside wrapped_f()
('Decorator arguments:', 'hello', 'world', 22)
('sayHello arguments:', 'a', 'different', 'set of', 'arguments')
After f(*args)
----------------After second sayHello() call----------------

'''