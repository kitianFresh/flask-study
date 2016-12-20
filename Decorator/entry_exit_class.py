# -*- coding: utf8 -*-

class entry_exit(object):

    def __init__(self, f):
        self.f = f

    def __call__(self):
        print("Entering", self.f.__name__)
        self.f()
        print("Exited", self.f.__name__)

@entry_exit
def func1():
    print("call func1()")

@entry_exit
def func2():
    print("call func2()")

func1()
func2()

'''
('Entering', 'func1')
call func1()
('Exited', 'func1')
('Entering', 'func2')
call func2()
('Exited', 'func2')
当 Python 解释器 读取到 @entry_exit 时， 就会寻找 entry_exit 了， 由于 entry_exit 是装饰器， 初始化需要参数 f， 
因此继续往下读取要被装饰的函数func1，func1 被解释器替换为 func1 = entry_exit(func1), 执行到 func1() 就是 func1.__call__()
你也许就会觉得，这不就是执行 func1 的时候，多加一个 entry_exit(func1)(), 其实就是函数式编程即把函数 func1 当参数传递。
当然你也可以从另一个层面来理解，就是以 @entry_exit 为代码主体，即把里面的 f 看成是 C 语言里的 micro 宏定义， 
把 func1 func2 看成实际的宏替换实例。例如 define micro 777 就是这里的 @entry_exit func1, 
只不过这里的 宏 替换换过程是 动态的，因为 C 语言是 静态 编译类型，Python 是 动态 解释类型语言嘛^_^

def bar(): pass
bar = staticmethod(bar)
等价于
@staticmethod
def bar(): pass

再来看看 decorator 的 @ 写法， 实际上是带领我们进入另一种 程序设计思维， 虽然本质上是 函数式 或者 宏替换。即 把 代码 运用到 代码 中。记住一个观点，
软件工程的所有设计方法，有99%其实是因为懒。即为了 少 写 代码。代码写的越少，越易读，易维护，易扩展，易重构。但是少写代码并不意味着你真的少写了代码，
实际上你看看开源社区，我们的代码 肯定是 越来越多的。但是 从 历史的 角度来看， 代码是越写越少。
'''