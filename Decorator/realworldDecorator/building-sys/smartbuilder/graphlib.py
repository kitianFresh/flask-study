# -*- coding: utf-8 -*-

from collections import defaultdict

class Graph:

    """ 一个关于构建任务之间关系的有向图. 
    
    一个任务是通过 hash 值直接获取的, 这里使用 python 的 dictionary key.
    """
    sort_key = None

    def __init__(self):
        # 使用 defaultdict 而不是 dict 的原因是, dict 对不存在 key 的访问 dict['key'] 访问会抛出 KeyError
        # defaultdict 当 key 不存在时, 会输出 空集合 set(). 这样代码会更加简练, Pythonic
        # 这里采用了同时存储 出度和入度 的冗余 hash 链表
        self._inputs_of = defaultdict(set)
        self._consequences_of = defaultdict(set)

    def sorted(self, nodes, reverse=False):
        nodes = list(nodes)
        try:
            nodes.sort(key=self.sort_key, reverse=reverse)
        except TypeError:
            pass
        return nodes

    def add_edge(self, input_task, consequence_task):
        """ 添加一条边: `consequece_task` 使用 `input_task` 的输出. """
        self._consequences_of[input_task].add(consequence_task)
        self._inputs_of[consequence_task].add(input_task)
    
    def remove_edge(self, input_task, consequence_task):
        self._consequences_of[input_task].remove(consequence_task)
        self._inputs_of[consequence_task].remove(input_task)

    def inputs_of(self, task):
        """
        按顺序返回 `task` 的所有输入
        """
        return self.sorted(self._inputs_of[task])
    
    def clear_inputs_of(self, task):

        input_tasks = self._inputs_of.pop(task, ()) # 删除所有的该任务的入度
        # 删除该任务在出度的贡献
        for input_task in input_tasks:
            self._consequences_of[input_task].remove(task)

    def edges(self):
        """ 返回所有的边, 结果是 由 ``(input_task, consequence_task)`` 组成的 tuples."""
        return [(a, b) for a in self.sorted(self._consequences_of)
                       for b in self.sorted(self._consequences_of[a])]
    def tasks(self):
        """返回图中所有的任务."""
        return self.sorted(set(self._inputs_of).union(self._consequences_of))

    def immediate_consequences_of(self, task):
        """Return the tasks that use `task` as an input."""
        return self.sorted(self._consequences_of[task])

    def recursive_consequences_of(self, tasks, include=False):
       
        def visit(task):
            visited.add(task)
            consequences = self._consequences_of[task]
            for consequence in self.sorted(consequences, reverse=True):
                if consequence not in visited:
                    visit(consequence)
            stack.insert(0, task)

        def generate_consequences_backwards():
            for task in self.sorted(tasks, reverse=True):
                visit(task)
                if include is False:
                    stack.remove(task)
        
        visited = set()
        stack =[]
        generate_consequences_backwards()
        return stack