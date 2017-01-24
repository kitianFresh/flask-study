# 函数式编程 functional programming

## 基本特征
 1. 函数是first-class citizen，即一等公民，他可以像变量一样使用
 2. 函数可以是参数
 3. 函数可以是返回值

## 支持函数式的语言
 * Java 1.7以前并不支持函数式，只能通过对象模仿函数式，1.8 开始引入匿名函数lambda，实现了部分支持函数式
 * C/C++不直接支持函数式，只能使用函数指针，但函数指针非常复杂
 * C# 也不直接支持，但是有一个delegate和函数指针比较类似
 * Python、Ruby、JavaScript是支持函数式的混合式语言
 * Golang 支持函数式编程
 * LISP 正统的纯正函数式语言

## Python 中的基本属性
1.赋值
函数是第一等公民(first-class citizen),是一个对象，可以像其他变量一样赋值，修改状态等

```python
def hello():
    print "hello, ustc"
func = hello
func()
func.__name__
```
2.嵌套定义
函数内部可以嵌套定义一个函数，这在C 和 Java 中是不允许的；

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
3.参数和返回
函数可以当参数传递给另一个函数，或者当做一个函数的返回值，我们称这样的函数为 High-order function；另外，经常见到的lambda表达式，这来源于[Lambda calculus](https://en.wikipedia.org/wiki/Lambda_calculus);我们不需要过多的理解他的数学理论，大部分情况下，lambda用来表示一个匿名纯函数(那些简单的，只用计算，而不需要IO的操作)；

```python
def my_map(operation, sequence):
    result = []
    for s in sequence:
        if isinstance(s, list):
            result.append(my_map(operation, s))
        else:
            result.append(operation(s))
    return result

l = [1,2,3,4,5,6]
n_l = [1,2,[3,4,[5,6]]]
print my_map(lambda x: x*x, l)
print my_map(lambda x: x*x, n_l)

print map(lambda x: x*x , l)
# print map(lambda x: x*x, n_l) #TypeError: can't multiply sequence by non-int of type 'list'

def outer():
    x = 1
    def inner():
        print x
    return inner
f = outer()
f()
```
4.闭包

闭包closure也是一个数学概念，但在这里我们只需要知道编程语言中是什么意思就行了；
我们来看一个奇特的现象，这个现象会结合函数式和变量生命周期来解释。既然 outer 已经调用完成了， 那么 x 的 生命周期 就结束了， 应该被销毁了， 
但是我们却可以在 f() 即 inner 函数内部继续访问到 x 即 outer 作用域内的 x；这个就是 Python 的闭包 closure。
>Python supports a feature called function closures which means that inner functions defined in non-global scope remember what their enclosing namespaces looked like at definition time.
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

5.mutability 
函数内部定义的嵌套函数不能直接写 immutable 对象；如果想要修改外层函数的变量值， 使用 mutable 对象如 container；

```python
def outer():
    count = 0
    def inner():
        # count += 1 #UnboundLocalError: local variable 'count' referenced before assignment
        return count
    return inner

counter = outer()
print counter()

def better_outer():
    count = [0]
    def inner():
        count[0] += 1
        return count[0]
    return inner

counter = better_outer()
print counter()
```
The following are immutable objects:
 * Numeric types: int, float, complex
 * string
 * tuple
 * frozen set
 * bytes
 
 The following objects are mutable:
 * list
 * dict
 * set
 * byte array

 [PYTHON OBJECTS: MUTABLE VS. IMMUTABLE](https://codehabitude.com/2013/12/24/python-objects-mutable-vs-immutable/)

## 函数式列举
### 斐波那契数列的跟踪
fib函数
```Python
def fib(n):
    if n is 0 or n is 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)
```
fib函数自己跟踪自己，C style 面向过程; 每次进入递归函数的时候，我们打印当前深度，并将深度加1；离开递归函数的时候，我们有打印深度，并将深度减1；

```python
indent = 0
def fib_verbose_tree(n):
    global indent 
    print '| ' * indent + '|--', 'fib', n
    indent += 1
    if n is 0 or n is 1:
        print '| ' * indent + '|--', 'return', repr(1)
        indent -= 1
        return 1
    else:
        value = fib_verbose_tree(n-1) + fib_verbose_tree(n-2)
        print '| ' * indent + '|--', 'return', repr(value)
        indent -= 1
        return value
print '-------------fib_verbose_tree-----------'
print fib_verbose_tree(4)
```
但是以上函数是冗杂的，他直接毁坏了原来的斐波那契函数的干净美感， 使得函数多了一些不需要的东西。如果我们需要随时可以查看递归树，或者选择不查看，那么就得写两个函数了；但是我们发现，以上C风格的栈跟踪，其实每次都是刚刚进入函数时，打印深度，深度增加，退出函数之前，打印深度，深度减少；他不就等价于，把打印深度，深度增加，提前到函数调用之前，而打印深度，深度减少，延迟到函数返回之后，其实表现结果是一样的，这就促使我们可以想到使用一个装饰函数来包裹fib；
 1. **函数用来包裹函数（high-order function），即函数的操作目标是函数，从而动态的修改函数。**
  * 完成一个栈跟踪函数，来包裹fib，从而实现分离，维护更加清晰的代码；
```python
def trace_tree(f):
    f.indent = 0
    def wrapped(n):
        print '| ' * f.indent + '|--', f.__name__, n
        f.indent += 1
        value = f(n)
        print '| ' * f.indent + '|--', 'return', repr(value)
        f.indent -= 1
        return value
    return wrapped

print '-------------trace_tree-----------'
fib = trace_tree(fib)
print fib(4)
```
跟进一步，我们还可以使用装饰函数，实现可插拔的动态规划编程，记录函数的返回结果，实现动态规划dp；

```python
def memoize(f):
    cache = {}
    def wrapped(n):
        if n not in cache:
            cache[n] = f(n)
        return cache[n]
    return wrapped

# print '-------------memoize_trace_tree-----------'
# fib = trace_tree(fib)
# fib = memoize(fib)
# print fib(4)
```
 2. **函数可以用来操作函数及数据（map-reduce），从而带来更加抽象和通用的接口；**
  * 如果函数可以当做参数，那么就可以很容易写出更加通用和抽象的底层代码，比如map reduce计算框架：
  * 实现一个简单的my_map函数，可以实现对嵌套列表的操作：
```python
def my_map(operation, sequence):
    result = []
    for s in sequence:
        if isinstance(s, list):
            result.append(my_map(operation, s))
        else:
            result.append(operation(s))
    return result

l = [1,2,3,4,5,6]
n_l = [1,2,[3,4,[5,6]]]
print my_map(lambda x: x*x, l)
print my_map(lambda x: x*x, n_l)

print map(lambda x: x*x , l)
# print map(lambda x: x*x, n_l) #TypeError: can't multiply sequence by non-int of type 'list'
```
 3. **递归函数的包装注意事项：确定你需要包装的是那一层次，特别是多层次的包装递归函数的时候，要分清包装函数到底包装到那一层次。**
 * 用函数式编程，实现一个分析函数总的执行时间的装饰器函数
```python
import time
def profile(f):
    def wrapped(n):
        start = time.time()
        value = f(n)
        end = time.time()
        print "time taken: %lf sec" % (end - start)
        return value
    return wrapped

print '-------------timing_trace_tree-----------'
fib = profile(memoize(trace_tree(fib)))
print fib(20)
```
以上这种写法到底能不能得到递归函数 fib(20) 的执行时间呢？ 其实这样写，会计算每一次递归从进入到返回的时间；最后计算的是不准确的，而且加入缓存后，遇到相同数计算时，计算过的已经被缓存，不需要再计算了；

因此，对递归函数的装饰器，要特别小心，
 - 如果你要包装递归函数，并且想知道每一步递归的具体调用情况，必须要让包装后的函数名和原来的递归函数名字一样，要不然被包装的递归函数只是在第一层包装了；
 - 如果不想知道递归细节，只想在递归最外层执行完毕后被包装，那么就不要用和递归函数同名的函数名字，这样里面的每一层调用还是调用他原来的本尊（未加工的那个原始的函数）。

```python
# print '-------------timing_trace_tree-----------'
# fib = memoize(trace_tree(fib))
# f = profile(fib)
# print f(20)
```
 
这里只要知道函数式编程的本质是 **函数是一等公民，可以像变量一样随时修改，赋值，还可以当参数和返回。** 分析函数式时，需要记住包装的函数之间是不断的赋值，返回；
 
例如 t = memoize(trace_tree(fib))
``` python
t = memoize(trace_tree(fib))
print t(4)
|-- fib 4
| |-- return 5
5
```
打印的只有第一层的，但是确实算出来了最终结果，这说明fib一定完成了调用，但是trace\_tree并没有，为什么？因为这里的trace\_tree
并没有被改名为fib啊，所以在第一层的trace\_tree打印之后，当递归进入下一层的时候，调用fib函数，可是fib函数是原来那个没有被装饰过的，
这就导致了看不到后面几层的调用过程了。如果你把先把trace_tree(fib)赋值给fib，然后再传递给memoize，就可以了，或者直接最终赋值fib
即 fib = trace_tree(fib) fib = memoize(fib)[如果这里改成f = memoize(fib) 呢？那结果就是可以trace，但是只有第一层会被缓存，即缓存失效了] 
或一步到位 fib = memoize(trace_tree(fib))

## 函数式总结
函数式和面向对象/面向过程的区别到底是什么？
 - 函数式其实更加偏向于计算和数学思维，相同的输入，相同的输出，即函数映射关系不变，计算结果就不会改变，不会发生死锁（其实，是解决的这种问题大多数不需要锁，因为closure是不允许改变原始数据的）
 - 面向过程和面向对象更加关注计算机指令的实现，需要你理解循环，语法等细节，他们关注的是解决问题的步骤，函数式编程你造样要使用循环，但是他不是思考的重点

不要太过于纠结他们有什么区别，所有的编程范式都不是非此即彼，水火不容，采用特定范式解决特定的问题才是好的。

我们可以看到，函数式编程中，函数不仅直接调用，也可以当成参数被其他函数调用。 因此，进一步，如果我不仅想把函数当参数，还想传入值，所以再封装一下，函数和值封装后是什么。
  * 函数->行为
  * 值->属性

这就是对象，而且比对象更厉害的是，他可以改变行为，随意组合行为，因为他的行为是一个函数，而函数式中，函数灵活改变，这个应对现在不断变化的需求就显得更加有用
将业务逻辑细化，抽象，封装成一个个对象，并借助语言，库，组件，框架等，将整个业务流程转化为对象之间的相互调用，这就是面向对象编程。
近年来大数据的兴起，数据的处理往往跟面向对象没关系，更多的是简单而大量的数据结构，借助map reduce这样的高阶函数处理更加方便，这也是函数式编程又火起来的原因

## 参考
 * [函数式编程](http://coolshell.cn/articles/10822.html)
 * [Functional Programming For The Rest of Us](http://www.defmacro.org/ramblings/fp.html)
 * [A practical introduction to functional programming](https://maryrosecook.com/blog/post/a-practical-introduction-to-functional-programming)
 * [Functional Programming HOWTO](https://docs.python.org/2/howto/functional.html#)
 * [A practical introduction to Functional Programming for Python coders](https://codesachin.wordpress.com/2016/04/03/a-practical-introduction-to-functional-programming-for-python-coders/)