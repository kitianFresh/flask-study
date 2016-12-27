# -*- coding: utf-8 -*-

# method decorator 如果没有其他参数，直接用 self 做func_wrapper()的参数，如果还有其他参数，
# 则用(*args, **kwargs)更加通用
def p_decorator(func):
   def wrapped(*args, **kwargs):
       return "<p>{0}</p>".format(func(*args, **kwargs))
   return wrapped

class Person(object):
    def __init__(self):
        self.name = "kinny"
        self.family = "Tian"

    @p_decorator
    def get_fullname(self):
        return self.name+" "+self.family

my_person = Person()

print my_person.get_fullname()