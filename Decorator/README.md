# Python Decorator & Closure

## 理解装饰器
### 1. function 函数 & nested_function
在Python 中， 函数是**first-class citizen**第一等公民， 即和其他变量一样可以赋值,而且还具有很多属性可以访问等。可以直接当做参数传递给另一个函数，可以当函数的返回值。
这在 C 语言中是没有的， C 语言只能间接通过函数指针来完成函数参数的传递。
```python
def 
```
但是，和C/Java不同的是，Python还支持在函数内部定义函数；
```python
def nested_function():
    def first_func():
        print "first_func"
    
    def second_func():
        print "second_func"

    first_func()
    second_func()

nested_function()
```
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
### 6. Decorator
什么是装饰器，就是装饰函数或者类的函数或类。那么他就必须接受 一个函数或者类当参数， 然后装饰它， 最后返回 装饰好的 函数或类。类比大象放冰箱分三步，decorator三步走：
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

@decorator
def decorated():
    # code
# 以上等价于
# decorated = decorator(decorated)
decorated()
```
以上是装饰器的本质吗？装饰器就是函数式编程而已？的确可以这么理解，但是这样说也不对，他只是一种叫法，虽然大多说时候，我们都用***装饰器实现了装饰器模式，但是装饰器并不仅仅体现了函数式编程***，
它体现的更加本质的东西是***一处代码被另一处代码动态修改或者说替换***，这也正是编译型语言做不到的事情，例如C/C++就做不到。一个***语言要想动态的修改自己，绝对需要靠虚拟机或者解释器在运行的时候来帮忙***，
编译器是没有办法做的；Java具有反射机制，动态产生和构造一个类，实际上就是因为它有一个虚拟机，虚拟机提供了这种接口。所以，解释型语言都具备很大的灵活性和可操作性。当然你也可以从另一个层面来理解装饰器，
就是以 decorator 为代码主体，即把里面的 decorator 看成是 C 语言里的 micro 宏定义， 把 decorated 看成实际的宏替换实例。例如 define micro 777 就是这里的 @decorator decorated, 
只不过这里的 宏 替换换过程是 动态的，因为 C 语言是 静态 编译类型，Python 是 动态 解释类型语言嘛^\_^;因此本质上就是***少写代码，动态修改*** ^\_^

### 7. Syntactic sugar!
Python allows you to simplify the calling of decorators using the @ symbol (this is called “pie” syntax).

#### 参考
 - [Decorators](http://python-3-patterns-idioms-test.readthedocs.io/en/latest/PythonDecorators.html)
 - [Understanding Python Decorators in 12 Easy Steps!](http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/#footnote_2)
 - [Python Decorators](https://pythonconquerstheuniverse.wordpress.com/2012/04/29/python-decorators/)
 - [Primer on Python Decorators](https://realpython.com/blog/python/primer-on-python-decorators/)web flask为例子讲解decorator使用场景
 - [guide-to-python-function-decorators](http://thecodeship.com/patterns/guide-to-python-function-decorators/)以html渲染为例子，还讲了functools.wraps的由来
 - [pep-0318](https://www.python.org/dev/peps/pep-0318/#current-syntax)
 
高级主题，对类进行装饰,以后再进一步学习，目前先理解到这里
Almost certainly, anything which could be done with class decorators could be done 
using metaclasses, but using metaclasses is sufficiently obscure that there is some 
attraction to having an easier way to make simple modifications to classes. 
For Python 2.4, only function/method decorators are being added.
 - [Python Decorators III: A Decorator-Based Build System](http://www.artima.com/weblogs/viewpost.jsp?thread=241209)一个基于装饰器的构建系统
 - [metaclasses-abc-class-decorators](http://intermediatepythonista.com/metaclasses-abc-class-decorators)
 - [Advanced Uses of Python Decorators](https://www.codementor.io/python/tutorial/advanced-use-python-decorators-class-function)
 - [Python decorators: metaprogramming with style](http://blog.thedigitalcatonline.com/blog/2015/04/23/python-decorators-metaprogramming-with-style/#.WGIjJ3V97CJ)

# Python property lazy

# Python generator yield

# Python contextmanager
