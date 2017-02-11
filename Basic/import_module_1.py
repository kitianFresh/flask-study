'''Some documentation for this file.'''
import pprint

print 'globals before def: %s\n' % pprint.pformat(globals(), indent=4)

def simple():
  print 'locals before a: %s\n' % locals()
  a = 'simple'
  print 'locals after a: %s\n' % locals()
  return a

print 'globals after def: %s\n' % pprint.pformat(globals(), indent=4)

simple()