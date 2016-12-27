def outer():
    x = 1
    def inner():
        print x
    return inner
f = outer()
f()
print f.func_closure

def nested_function():
    def first_func():
        print "first_func"
    
    def second_func():
        print "second_func"

    first_func()
    second_func()

nested_function()