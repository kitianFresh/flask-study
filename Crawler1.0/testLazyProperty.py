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