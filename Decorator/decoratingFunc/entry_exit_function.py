# -*- coding: utf8 -*-

def entry_exit(f):
    def new_f():
        print("Entring", f.__name__)
        f()
        print("Exited", f.__name__)
        #new_f.__name__ = f.__name__
    return new_f
    #return new_f()

@entry_exit
def func1():
    print("call func1()")

@entry_exit
def func2():
    print("call func2()")

func1()
func2()
print(func1.__name__)

'''
('Entring', 'func1')
call func1()
('Exited', 'func1')
('Entring', 'func2')
call func2()
('Exited', 'func2')
new_f
当 Python 解释器 读取到 @entry_exit 时， 就会寻找 entry_exit 了， 由于 entry_exit 是装饰器，调用需要参数 f， 
因此继续往下读取要被装饰的函数func1，func1 被解释器替换为 func1 = entry_exit(func1), 右值返回的是 new_f， 
因此 func1.__name__ 是 new_f 了。entry_exit() 可以理解为 closure， 因为 他包裹了 new_f ， 并返回 new_f， 
注意是 new_f 而不是 new_f(), 后者是调用这个函数了，前者是返回这个函数对象。
更换成 return new_f(),结果就是 NoneType ， 因为 new_f() 调用后，没有返回 Python 默认返回 None
('Entring', 'func1')
call func1()
('Exited', 'func1')
('Entring', 'func2')
call func2()
('Exited', 'func2')
Traceback (most recent call last):
  File "entry_exit_function.py", line 20, in <module>
    func1()
TypeError: 'NoneType' object is not callable
'''