# Python Decorator & Closure

## 预备知识
### 1. function 函数
在Python 中， 函数是first-class citizen第一等共鸣， 即和其他变量一样具有属性，可以赋值等。可以直接当做参数传递给另一个函数，可以当函数的返回值。
这在 C 语言中是没有的， C 语言只能间接通过函数指针来完成函数参数的传递。
### 2. Scope 变量作用域
Python 变量作用域 也遵循局部和全局的访问模式。这和 C，Java等都是一样的。函数内部变量都是局部变量（包括参数），位置和整个py文件同级的变量是全局变量。
```Python
global_var = "This is a global variable"
def func():
    print locals()
func()
print globals()

'''
{}
{'__builtins__': <module '__builtin__' (built-in)>, 'global_var': 'This is a global variable', '__file__': 'test.py', '__
package__': None, 'func': <function func at 0x7f264f2815f0>, '__name__': '__main__', '__doc__': None}
'''
```
### 3. Scope 变量解析规则
访问时，一定是从内到外寻找变量，赋值时一定是当做局部变量即当所处代码块同级变量处理。Python 支持在函数内部定义函数。
```Python
global_var = "This is a global variable"
def func():
    global_var = "Try to change global_var"
    print locals()
func()
print globals()
'''
{'global_var': 'Try to change global_var'}
{'__builtins__': <module '__builtin__' (built-in)>, 'global_var': 'This is a global variable', '__file__': 'test.py', '__
package__': None, 'func': <function func at 0x7fbd8a05a5f0>, '__name__': '__main__', '__doc__': None}
'''
```
### 4. 变量生命周期 lifetime
Python 局部变量的生命周期也是在函数调用时被创建，调用完成后被销毁
```Python
def func():
    x = 1
func()
print x

'''
Traceback (most recent call last):
  File "test.py", line 4, in <module>
    print x
NameError: name 'x' is not defined
'''
```
### 5. 闭包 Closure
我们来看一个奇特的现象，这个现象会结合函数式和变量生命周期来解释。既然 outer 已经调用完成了， 那么 x 的 生命周期 就结束了， 应该被销毁了， 
但是我们却可以在 f() 即 inner 函数内部继续访问到 x 即 outer 作用域内的 x；这个就是 Python 的闭包 closure。
Python supports a feature called function closures which means that inner functions 
defined in non-global scope remember what their enclosing namespaces looked like at definition time.
```
def outer():
    x = 1
    def inner():
        print x
    return inner
f = outer()
f()
f.func_closure

'''
1
(<cell at 0x7fe28f4f4328: int object at 0x22f6158>,)
'''
```
### Decorator
什么是装饰器，就是装饰函数或者类的函数或者类。那么他就必须接受 一个函数或者类当参数， 然后装饰它， 最后返回 装饰好的 函数或类。类比大象放冰箱分三步，decorator三步走：
 1. 把 **被装饰者** **传递**给 **装饰者**;
 2. 在 装饰者 **内部装饰** 这个 被装饰者。由于 需要返回一个 被装饰的 对象， 因此 **在装饰者 内部 一定至少会 定义一个新的 函数**;
 3. **返回 装饰者 新定义的 函数对象 即经过装饰后的对象**;
```Python
def decorator(original_func):

    def decorated(*args, **kwargs):
        # code before original_func
        original_func(*args, **kwargs)
        # code after original_func
    return decorated

def decorated():
    # code

decorated = decorator(decorated)
decorated()
```

## 参考
 - [Decorators](http://python-3-patterns-idioms-test.readthedocs.io/en/latest/PythonDecorators.html)
 - [Understanding Python Decorators in 12 Easy Steps!](http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/#footnote_2)
 - [Python Decorators](https://pythonconquerstheuniverse.wordpress.com/2012/04/29/python-decorators/)
 - [Primer on Python Decorators](https://realpython.com/blog/python/primer-on-python-decorators/)
 - [类属性的延迟计算](http://www.spiderpy.cn/blog/5/)