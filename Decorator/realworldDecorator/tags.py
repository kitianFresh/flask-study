# -*- coding: utf-8 -*-

def p_decorator(func):
    def wrapped(text):
        '''
        p_decorator
        '''
        return "<p>{0}</p>".format(func(text))
    return wrapped

def strong_decorator(func):
    def wrapped(text):
        '''
        strong_decorator
        '''
        return "<strong>{0}</strong>".format(func(text))
    return wrapped

def div_decorator(func):
    def wrapped(text):
        '''
        div_decorator
        '''
        return "<div>{0}</div>".format(func(text))
    return wrapped

@div_decorator
@p_decorator
@strong_decorator
def get_text(name):
    '''
    get text of a name
    '''
    return "vivalavida, {0} ".format(name)

print get_text("world")
print get_text.__name__, get_text.__doc__, get_text.__module__
#get_text = div_decorator(p_decorator(strong_decorator(get_text)))

# 上面的decorator还是不够抽象，因为写的代码还是一种重复，结构都是一样的，
# 就是包装的tag不一样，因此这个工作再一次抽象出来统一用参数处理,就可以需要带参数的decorator了

def tags(tag_name):
    def tags_decorator(func):
        def wrapped(name):
            '''
            tags_decorator
            '''
            return "<{0}>{1}<{0}>".format(tag_name, func(name))
        wrapped.__name__ = func.__name__
        wrapped.__doc__ = func.__doc__
        wrapped.__module__ = func.__module__
        return wrapped
    return tags_decorator

@tags('div')
@tags('p')
def get_info(name):
    '''
    get info of a name
    '''
    return "vivalavida, "+ name


print get_info("kinny")
print get_info.__name__, get_info.__doc__, get_info.__module__

# 但是当你打印get_info.__name__的时候，发现名字改变了
# 这样就非常不利于调试了，比如你的get_info 函数发生错误， 打印出来出错信息是在装饰器上，
# 因此我们在返回装饰后的函数时，应该修改他的相关信息，使其与真实的被装饰函数一致;

# 但实际上这个工作也是重复的，如果每一个装饰器都得多些这几行代码，真是不可忍受的，
# 注意记住装饰器的本质，用一个代码动态替换或这说修改另一处代码，从而减少重复写代码，下面我们就来写一个装饰器给装饰器使用
'''
def my_wraps(original_func):
    def decorator(decorator_func):
        def wrapped(*args):
            return decorator_func(*args)
        wrapped.__name__ = original_func.__name__
        wrapped.__doc__ = original_func.__doc__
        wrapped.__module__ = original_func.__module__
        return wrapped
    return decorator
'''

def my_wraps(original_func):
    def decorator(decorator_func):
        decorator_func.__name__ = original_func.__name__
        decorator_func.__doc__ = original_func.__doc__
        decorator_func.__module__ = original_func.__module__
        return decorator_func
    return decorator

def tags1(tag_name):
    def tags_decorator(func):
        @my_wraps(func)
        def wrapped(name):
            '''
            tags1_decorator
            '''
            return "<{0}>{1}<{0}>".format(tag_name, func(name))
        return wrapped
    return tags_decorator

@tags1('div')
@tags1('p')
def get_info1(name):
    '''
    get info1 of a name
    '''
    return "vivalavida1, "+ name

print get_info1("kinny1")
print get_info1.__name__, get_info1.__doc__, get_info1.__module__

# 其实，Python 已经内置了 一个 wraps 装饰器 functools.wraps ，可以实现保存函数信息的功能

'''
Almost certainly, anything which could be done with class decorators could be done 
using metaclasses, but using metaclasses is sufficiently obscure that there is some 
attraction to having an easier way to make simple modifications to classes. 
For Python 2.4, only function/method decorators are being added.
'''
# method decorator 如果没有其他参数，直接用 self 做func_wrapper()的参数，如果还有其他参数，
# 则用(*args, **kwargs)更加通用
def p_decorate(func):
   def func_wrapper(*args, **kwargs):
       return "<p>{0}</p>".format(func(*args, **kwargs))
   return func_wrapper

class Person(object):
    def __init__(self):
        self.name = "John"
        self.family = "Doe"

    @p_decorate
    def get_fullname(self):
        return self.name+" "+self.family

my_person = Person()

print my_person.get_fullname()