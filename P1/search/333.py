visit = {(3,1): False, (3,2): False, (3, 3): False }
corners = ((1,1), (3,1), (3, 2), (3, 3))
c = ((1,1), (1,2), (3, 1), (3, 3))
a=(1,1)
a=set(a)
a.add(c)
print a
print c[1]
print c



l=[]


s=((1,3),{(3,1): False, (3,2): False, (3, 3): False })
t=((333,3),{(3,1): False, (3,2): False, (3, 3): False })
l.append(s)
l.append(t)
print l
print l[1]

if t in l:
    print "333"
