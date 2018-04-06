import itertools
'''a = [1,2,3]
b = a
b.remove(1)
print a
print b'''

t = [(1,2),(2,3),(3,3)]

a = list(itertools.product(t, repeat=3))
print a

b = itertools.product(t, repeat=2)

for i in 5:
	print i