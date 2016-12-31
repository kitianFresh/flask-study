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
 1. 赋值
 2. 嵌套定义
 3. 返回
 4. 闭包

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
fib函数自己跟踪自己，C style 面向过程
```Python
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
 1. 函数用来包裹函数（high-order function），即函数的操作目标是函数，从而动态的修改函数。
  * 完成一个栈跟踪函数，来包裹fib，从而实现分离，维护更加清晰的代码；
```
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
 2. 函数可以用来操作函数及数据（map-reduce），从而带来更加抽象和通用的接口；
  * 如果函数可以当做参数，那么就可以很容易写出更加通用和抽象的底层代码，比如map reduce计算框架：
  * 实现一个简单的my_map函数，可以实现对嵌套列表的操作：
```Python
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
## 函数式总结
函数式和面向对象/面向过程的区别到底是什么？
函数式其实更加偏向于计算和数学思维，相同的输入，相同的输出，即函数映射关系不变，计算结果就不会改变，不会发生死锁（其实，是解决的这种问题大多数不需要锁，因为closure是不允许改变原始数据的）
面向过程和面向对象更加关注计算机指令的实现，需要你理解循环，语法等细节，他们关注的是解决问题的步骤，函数式编程你造样要使用循环，但是他不是思考的重点
不要太过于纠结他们有什么区别，所有的编程范式都不是非此即彼，水火不容，采用特定范式解决特定的问题才是好的。

我们可以看到，函数式编程中，函数不仅直接调用，也可以当成参数被其他函数调用。 因此，进一步，如果我不仅想把函数当参数，还想传入值，所以再封装一下，函数和值封装后是什么。
函数->行为
值->属性
没错就是这就是对象，而且比对象更厉害的是，他可以改变行为，随意组合行为，因为他的行为是一个函数，而函数式中，函数灵活改变，这个应对现在不断变化的需求就显得更加有用
将业务逻辑细化，抽象，封装成一个个对象，并借助语言，库，组件，框架等，将整个业务流程转化为对象之间的相互调用，这就是面向对象编程。
近年来大数据的兴起，数据的处理往往跟面向对象没关系，更多的是简单而大量的数据结构，借助map reduce这样的高阶函数处理更加方便，这也是函数式编程又火起来的原因