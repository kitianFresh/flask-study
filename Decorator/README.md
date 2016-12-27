# Python Decorator & Closure

## 预备知识
### 1. function 函数 & nested_function
在Python 中， 函数是first-class citizen第一等公民， 即和其他变量一样具有属性，可以赋值等。可以直接当做参数传递给另一个函数，可以当函数的返回值。
这在 C 语言中是没有的， C 语言只能间接通过函数指针来完成函数参数的传递。但是，和C/Java不同的是，Python还支持在函数内部定义函数；
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
以上是装饰器的本质吗？装饰器就是函数式编程而已？的确可以这么理解，但是这样说也不对，他只是一种叫法，虽然大多说时候，我们都用**装饰器实现了装饰器模式，但是装饰器并不仅仅体现了函数式编程**，
它体现的更加本质的东西是**一处代码被另一处代码动态修改或者说替换**，这也正是编译型语言做不到的事情，例如C/C++就做不到。一个**语言要想动态的修改自己，绝对需要靠虚拟机或者解释器在运行的时候来帮忙**，
编译器是没有办法做的；Java具有反射机制，动态产生和构造一个类，实际上就是因为它有一个虚拟机，虚拟机提供了这种接口。所以，解释型语言都具备很大的灵活性和可操作性。当然你也可以从另一个层面来理解装饰器，
就是以 decorator 为代码主体，即把里面的 decorator 看成是 C 语言里的 micro 宏定义， 把 decorated 看成实际的宏替换实例。例如 define micro 777 就是这里的 @decorator decorated, 
只不过这里的 宏 替换换过程是 动态的，因为 C 语言是 静态 编译类型，Python 是 动态 解释类型语言嘛^\_^;因此本质上就是**少写代码，动态修改** ^\_^
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


### Python 懒加载属性 lazy property
&emsp;&emsp;eager/lazy load/compute/write是计算机系统优化的一个重要技巧（eager还是lazy需要结合场景权衡，他们各有利弊），几乎所有的系统都会出现这个词，包括操作系统，比如虚拟内存中的页面延迟加载，只有当程序真正访问到该页时才会引发页面加载到内存。
也就是某个属性或者数据，初始化或者计算非常耗时，那么系统在未使用他的情况下，就不加载他，直到首次使用才加载，并且缓存起来供以后使用（前提是不再被替换掉）。那么具体到我们写一个类，
类的某个属性我们想实现延迟加载怎么办呢？
&emsp;&emsp;如果你写过Java的单例模式，就会知道其中一种写法就是先声明一个null的成员，然后在实例化中有如下代码，这个可以说就是lazy load 最最简单的模型了。这里就实现了类的实例初始化
时不加载该成员，直到首次使用也就是显式调用时才加载。[java-tip-67--lazy-instantiation](http://www.javaworld.com/article/2077568/learn-java/java-tip-67--lazy-instantiation.html)是一篇关于lazy instanciation in java的文章。
比较麻烦就是，Java中要实现某成员属性的延迟加载，访问必须使用get方法，而不能直接Object.property
``` 
if instance == null
    instance = new instance()
return instance
``` 
Python 中同样，需要对一个类的某些属性进行 lazy load 的话，Python 提供了 @property 的 snytax sugar; 使得我们不用通过方法调用，也能实现访问 lazy property。
```Python
# -*- coding: utf8 -*-

def some_timing_or_spacing_operation():
    print "some_timing_or_spacing_operation"
    return 6666

class RawLazyClass(object):
    '''
    Java 类似的写法
    '''
    def __init__(self):
        self._lazy_value = None
    @property
    def lazy_value(self):
        if self._lazy_value is None:
            self._lazy_value = some_timing_or_spacing_operation()
        return self._lazy_value


# 这个虽然实现了 Python 方式的 lazy_property， 但是每一次都要重写 属性检查部分。
class AttrLazyClass(object):

    '''
    python 写法
    '''
    def __init__(self):
        pass
    
    @property
    def lazy_value(self):
        # 不能写成 if hasattr(self, '_lazy_value') is None， 返回的是bool:
        if not hasattr(self, '_lazy_value'):
            setattr(self, '_lazy_value', some_timing_or_spacing_operation())
        return getattr(self, '_lazy_value')

# 前面两种写法还有一个缺点就是，必须把 lazy_value 和 函数名字区分开， 否则 AttributeError: can't set attribute，因为 名字一样的话
# 变量就和函数混淆了

# 下面做成decorator之后， 就可以实现通用的 lazy_property 了， 可以减少重复的代码

# 函数版 decorator， 这个本质上和 AttrLazyClass 里的 lazy_value没有区别，如果使用他做装饰器，就是 
# 解释器执行到@lazy_property def lazy_value(self): 时，再一次self.lazy_value = lazy_property(self.lazy_value);实际上还是一个函数
# 只是这个函数被重新定义了，这就是装饰器的魅力所在，装饰器三步走，扔进去，装饰，提出来
def lazy_property(func):
    # 这里 属性名 也不能和 方法重名，否则 AttributeError: can't set attribute
    attr_name = "_" + func.__name__

    @property
    def _lazy_property(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, func(self))
        return getattr(self, attr_name)
    return _lazy_property

class MagicLazyClass(object):

    '''
    Python magic snytax sugar, use decorator
    '''

    def __init__(self):
        pass

    @lazy_property
    def lazy_value(self):
        return some_timing_or_spacing_operation()

# 类版 decorator，这里需要了解什么叫 descriptor, 因为必须要用 descriptor 才能实现类版本的 lazy_property decorator
# 使用这个， 解释器在执行到 @LazyProperty def lazy_value(self): 时，就 执行 self.lazy_value = LazyProperty(self.lazy_value)
# 注意此时，实际上 self.lazy_value本来是函数，现在变成什么了？ 变成了 LazyProperty 类对象了！！！他就是传说中 descriptor
class LazyProperty(object):
    """
    LazyProperty
    """

    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            # 这里可以重名， 因为这里的 self.lazy_value已经变成成员变量了
            setattr(instance, self.func.__name__, value)
            return value

class AnotherMagicLazyClass(object):

    '''
    Python magic snytax sugar, use decorator
    '''

    def __init__(self):
        pass

    @LazyProperty
    def lazy_value(self):
        return some_timing_or_spacing_operation()

class YetAnotherMagicLazyClass(object):

    '''
    Python magic snytax sugar, use decorator
    '''

    def __init__(self):
        self.lazy_value = 777

    @LazyProperty
    #@lazy_property 报错 AttributeError: can't set attribute
    def lazy_value(self):
        return some_timing_or_spacing_operation()

r = RawLazyClass()
print r.__dict__
print r.lazy_value
print r.__dict__
print "---------------------------------------------"

a = AttrLazyClass()
print a.__dict__
print a.lazy_value
print a.__dict__
print "---------------------------------------------"

m = MagicLazyClass()
print m.__dict__
print m.lazy_value
print m.__dict__
print "---------------------------------------------"

am = AnotherMagicLazyClass()
print am.__dict__
print am.lazy_value
print am.__dict__
print "---------------------------------------------"

yam = YetAnotherMagicLazyClass()
print yam.__dict__
print yam.lazy_value
print yam.__dict__

'''
{'_lazy_value': None}
some_timing_or_spacing_operation
6666
{'_lazy_value': 6666}
---------------------------------------------
{}
some_timing_or_spacing_operation
6666
{'_lazy_value': 6666}
---------------------------------------------
{}
some_timing_or_spacing_operation
6666
{'_lazy_value': 6666}
---------------------------------------------
{}
some_timing_or_spacing_operation
6666
{'lazy_value': 6666}
---------------------------------------------
{'lazy_value': 777}
777
{'lazy_value': 777}

'''
```


### data model in python2
 - [类属性的延迟计算](http://www.spiderpy.cn/blog/5/)
 - [Python Data Model](https://docs.python.org/2/reference/datamodel.html)
 - [python-class-attributes-an-overly-thorough-guide](https://www.toptal.com/python/python-class-attributes-an-overly-thorough-guide)
 - [Accessing attributes in Python](http://blog.thedigitalcatonline.com/blog/2015/01/12/accessing-attributes-in-python/#.WFpm-3V97CI)
 - [Introduction to Python: Class 5](http://www2.lib.uchicago.edu/keith/courses/python/class/5/##classinst)
 - [ dictproxyhack, or: ActiveState Code considered harmful](https://eev.ee/blog/2013/08/05/dictproxyhack-or-activestate-code-considered-harmful/##dictproxy)
When you try to access an attribute from an instance of a class, it first looks at its instance namespace. If it finds the attribute, it returns the associated value. If not, it then looks in the class namespace and returns the attribute (if it’s present, throwing an error otherwise)
But when you assign a value to an attribute from a class, with the class's instance.attribute, then it will be dynamically assigned to instance's attribute

### Python descriptor
Python descriptor 的引入，其实是为了让对象的成员变量可以拥有行为；听上去很难懂。成员变量如果是一个对象，那他不就绑定了行为了么。从这个角度解释就直接给初学者一个
很大的门槛。我们以 对象 成员变量需要类型检查为例来解释。
```
>>> class a(object): pass
>>> a.__dict__['wut'] = 4
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'dictproxy' object does not support item assignment
>>> setattr(a, 'wut', 7)
>>> a.wut
7
```
#### 参考
 - [Python Descriptors Demystified](http://nbviewer.jupyter.org/urls/gist.github.com/ChrisBeaumont/5758381/raw/descriptor_writeup.ipynb)
 - [Classes and Objects II: Descriptors](http://intermediatepythonista.com/classes-and-objects-ii-descriptors)
 - [Decorators and Descriptors](http://www.ianbicking.org/blog/2008/10/decorators-and-descriptors.html)
