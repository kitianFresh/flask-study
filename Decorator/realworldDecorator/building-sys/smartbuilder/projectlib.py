# -*- coding: utf-8 -*-

from contextlib import contextmanager
from collections import namedtuple
from functools import wraps
from .graphlib import Graph

_unavailable = object()


class Project:

    def __init__(self):
        self._graph = Graph()
        self._graph.sort_key = task_key
        self._cache = {}
        self._cache_on = True
        self._task_stack = []
        self._todo = set()
        self._trace = None

    def start_tracing(self):
        """ 开始追踪记录每一个 被 project 调用的 task"""
        self._trace = []

    def stop_tracing(self, verbose=False):
        """停止追踪任务调用, 返回调用关系写入文本.

        """
        text = '\n'.join(
            '{}{} {}'.format(
                '. ' * depth,
                'calling' if not_available else 'returning cached',
                task) for (depth, not_available, task) in self._trace
                if verbose or not_available
        )
        self._trace = None
        return text

    def _add_task_to_trace(self, task, return_value):
        """添加一个任务到当前运行的任务轨迹."""
        tup = (len(self._task_stack), return_value is _unavailable, task)
        self._trace.append(tup)

    def task(self, task_function):
        """装饰器函数,用来装饰该项目中的任务.

        
        """
        @wraps(task_function)
        def wrapper(*args):
            task = Task(wrapper, args)

            if self._task_stack:
                self._graph.add_edge(task, self._task_stack[-1])

            return_value = self._get_from_cache(task)
            if self._trace is not None:
                self._add_task_to_trace(task, return_value)

            if return_value is _unavailable:
                self._graph.clear_inputs_of(task)
                self._task_stack.append(task)
                try:
                    return_value = task_function(*args)
                finally:
                    self._task_stack.pop()
                self.set(task, return_value)
                
            return return_value

        return wrapper

    def _get_from_cache(self, task):
        """返回给定 `task` 的输出.

        如果无法查到一个现有的有效的 任务cache, 就返回 单例 _unavailable.
        """
        if not self._cache_on:
            return _unavailable
        if task in self._todo:
            return _unavailable
        return self._cache.get(task,_unavailable)

    @contextmanager
    def cache_off(self):
        """Context manager, 强制让 任务真正被调用.

        尽管project 已经缓存了某个任务的输出结果, 
        在这个上下文管理器中再次运行这个任务将会让project真正再次调用这个任务.而不是使用缓存!

            with project.cache_off():
                my_task()
        """
        original_value = self._cache_on
        self._cache_on = False
        try:
            yield
        finally:
            self._cache_on = original_value

    def set(self, task, return_value):
        """添加 `task` 的运行结果值 `return_value` 到 输出值缓存中.

        这里我们有机会比较新值和上一次任务返回结果的旧值, 
        从而决定那些使用 `task` 作为输入的任务集合是否需要被
        加入到 todo 列表中重新进行计算
        """
        self._todo.discard(task)
        if (task not in self._cache) or (self._cache[task] != return_value):
            self._cache[task] = return_value
            self._todo.update(self._graph.immediate_consequences_of(task))

    def invalidate(self, task):
        """标记 `task` 需要重新计算, 这是为了下一次 `rebuild()`.

        有两种方式 能够让 准备调用 `rebuild()` 的代码发出信号, 指明给定的任务缓存值已经不再有效了.  
        第一种, 直接手动 使用 `set()` 方法单方面装载新值到我们的缓存中; 第二种, 调用 `rebuild()` 方法
        invalidate 这个 `task`, 当 `rebuild()` 下一次运行的时候, 自己调用 这个 任务. 
        """
        self._todo.add(task)

    def rebuild(self):
        """重构所有过期的任务直到所有任务都是最新的.

        如果最近没有任何改变, 那么我们的 to-do 列表中将都是空的,这个方法会立即返回.
        否则, 我们取出 todo 中的所有任务, 并找到每一个任务的下游任务,即他会影响到的任务,
        调用每个任务的 `get()` 来强制重新计算每个要么已经失效而被放入todo的任务,
        要么因为todo列表前面几个任务被重新计算而失效的新任务.

        除非调用图中存在环, 否则一定会返回.
        """

        while self._todo:
            tasks = self._graph.recursive_consequences_of(self._todo, True)
            # print tasks[0]
            for function, args  in tasks:
                function(*args)

# Helper functions.

def task_key(task):
    """Return a sort key for a given task."""
    function, args = task
    return function.__name__, args


class Task(namedtuple('Task', ('task_function', 'args'))):
    """
    把一个 函数调用 转变为一个 二元 tuple 任务

    给定 任务函数 和 一个参数列表, 返回一个 二元tuple.
    """
    __slots__ = ()

    def __new__(cls, task_function, args):
        try:
            hash(args)
        except TypeError as e:
            raise ValueError('arguments to project tasks must be immutable and hashable, not the {}'.format(e))
        
        return super(Task, cls).__new__(cls, task_function, args)
    
    def __repr__(self):
        "语法糖, 任务的源代码表示"

        return '{}({})'.format(self.task_function.__name__,
                              ', '.join(repr(arg) for arg in self.args))