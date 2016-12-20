# -*- coding: utf8 -*-

def decorator_function_with_arguments(arg1, arg2, arg3):
    def wrap(f):
        print("Enter wrap()")
        
        def wrapped_f(*args):
            print("Inside wrapped_f()")
            print("Decorator arguments: ", arg1, arg2, arg3)
            f(*args)
            print("After f(*args)")
        
        print("Exit wrap()")
        return wrapped_f

    return wrap

@decorator_function_with_arguments("hello", "world", 22)
def sayHello(a1, a2, a3, a4):
    print('sayHello arguments:', a1, a2, a3, a4)

print("After decoration")

print("----------------Preparing to call sayHello()----------------")
sayHello("say", "hello", "argument", "list")
print("----------------After first sayHello() call----------------")
sayHello("a", "different", "set of", "arguments")
print("----------------After second sayHello() call----------------")

'''
Enter wrap()
Exit wrap()
来看看常见的函数decorator为啥都要写几层包裹函数，这是很多例子都有的，但是没告诉你为啥要这样写。
Python 解释器读取到 @decorator_function_with_arguments("hello", "world", 22) 时，首先查找 decorator_function_with_arguments 并调用，
但是 Python 知道这是一个装饰器啊，他还需要一个 被装饰的函数 f 做参数，和 class decorator 一样， 
在完成 dfwa = decorator_function_with_arguments(arg1, arg2, arg3) 之后，继续 寻找 f， 然后 f = dfwa(f), 此时还是装饰过程， 因此 返回的
还必须是 callable 对象，即函数。 也就是说， Python 的 带参数装饰器 解释过程 就是 f = dfwa(arg)(f) => f() 模型，三个调用才发生真正的调用，因此
function decorator 里面 必须是 嵌套 2 层 wrap func  
After decoration
----------------Preparing to call sayHello()----------------
Inside wrapped_f()
('Decorator arguments: ', 'hello', 'world', 22)
('sayHello arguments:', 'say', 'hello', 'argument', 'list')
After f(*args)
----------------After first sayHello() call----------------
Inside wrapped_f()
('Decorator arguments: ', 'hello', 'world', 22)
('sayHello arguments:', 'a', 'different', 'set of', 'arguments')
After f(*args)
----------------After second sayHello() call----------------
'''