from collections import deque
from pprint import pprint

d = deque()
d.append('a')
d.appendleft('b')

pprint(globals())