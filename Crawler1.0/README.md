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
