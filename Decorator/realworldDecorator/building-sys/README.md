
```python
{('tutorial.rst', 'tutorial.html'),
    ('index.rst', 'index.html'),
    ('api.rst', 'api.html')}
```


```python
{'tutorial.rst': {('tutorial.rst', 'tutorial.html')},
'tutorial.html': {('tutorial.rst', 'tutorial.html')},
'index.rst': {('index.rst', 'index.html')},
'index.html': {('index.rst', 'index.html')},
'api.rst': {('api.rst', 'api.html')},
'api.html': {('api.rst', 'api.html')}}
```


```python
incoming = {
        'tutorial.html': {'tutorial.rst'},
        'index.html': {'index.rst'},
        'api.html': {'api.rst'},
        }

outgoing = {
    'tutorial.rst': {'tutorial.html'},
    'index.rst': {'index.html'},
    'api.rst': {'api.html'},
    }
```

```python
#python2 写法
return super(Task, self).__new__(cls, task_function, args)

#python3 写法
return super().__new__(cls, task_function, args)

```