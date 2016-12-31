# -*- coding: utf-8 -*-

def exp(x, n):
    if n == 0:
        return 1

    else:
        return x * exp(x, n-1)

print exp(3,5)

def fast_exp(x, n):
    if n == 0:
        return 1

    if n % 2 == 0:
        return fast_exp(x*x, n/2)
    else:
        return x * fast_exp(x, n-1)
    
print fast_exp(3,5)

def flatten_list(nested_list):
    if len(nested_list) == 0:
        return None
    result = []
    for l in nested_list:
        if isinstance(l, list):
            result.extend(flatten_list(l))
        else:
            result.append(l)
    return result

l = [[1,2,3], [4,5,[6,7,8]]]
print flatten_list(l)


def flatten_dict(nested_dict):
    if len(nested_dict) == 0:
        return None
    result = {}
    for k,v in nested_dict.items():
        if isinstance(v, dict):
            sub_dict = flatten_dict(v)
            for sub_k, sub_v in sub_dict.items():
                result[k+'.'+sub_k] = sub_v
        else:
            result[k] = v 
    return result

d = {'a': 1, 'b': {'x': 2, 'y': 3}, 'c': {'x': 4, 'y': {'sigma': 5, 'mu': 6}}}
print flatten_dict(d)

def unflatten_dict(d):
    if len(d) == 0:
        return None
    pass

def treemap(f, nested_list):
    result = []
    for l in nested_list:
        if isinstance(l, list):
            result.append(treemap(f, l))
        else:
            result.append(f(l))
    return result

print treemap(lambda x: x*x, [1, 2, [3, 4, [5]]])

def tree_reverse(nested_list):
    nested_list.reverse()
    for l in nested_list:
        if isinstance(l, list):
            tree_reverse(l)
    return nested_list

print tree_reverse([[1, 2], [3, [4, 5]], 6])

def json_encode(data):
    if isinstance(data, bool):
        if data:
            return "true"
        else:
            return "false"

    elif isinstance(data, (int, float)):
        return str(data)

    elif isinstance(data, str):
        return '"' + escape_string(data) + '"'

    elif isinstance(data, list):
        return "[" + ", ".join(json_encode(d) for d in data) + "]"

    elif isinstance(data, dict):
        return "{" + ", ".join(['"' + escape_string(k) + '"'+": "+json_encode(v) for k, v in data.items()]) + "}"

    else:
        raise TypeError("%s is not JSON serializable" % repr(data))

def escape_string(s):
    s = s.replace('"', '\\"')
    s = s.replace("\t", "\\t")
    s = s.replace("\n", "\\n")
    return s

d = {
        "name": "Advanced Python Training",
        "date": "October 13, 2012",
        "completed": False,
        "instructor": {
            "name": "Anand Chitipothu",
            "website": "http://anandology.com/"
        },
        "participants": [
            {
                "name": 1,
                "email": "email1@example.com"
            },
            {
                "name": 2,
                "email": "email2@example.com"
            }
        ]
    }
print json_encode(d)


def fib(n):
    if n is 0 or n is 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

print 'fib', fib(3)

def fib_verbose(n):
    print fib_verbose.__name__, n
    if n is 0 or n is 1:
        print 'return', repr(1)
        return 1
    else:
        value = fib_verbose(n-1) + fib_verbose(n-2)
        print 'return', repr(value)
        return value
print '-------------fib_verbose-----------'
print fib_verbose(3)

def trace(f):
    def wrapped(n):
        print f.__name__, n 
        value = f(n)
        print 'return', repr(value)
        return value
    return wrapped

print '-------------trace_fib-----------'
fib = trace(fib)
print fib(3)

