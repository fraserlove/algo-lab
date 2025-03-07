from autodiff import Value

a = Value(2.0, label='a')
b = Value(-3.0, label='b')
c = Value(10.0, label='c')
f = Value(-2.0, label='f')
e = a * b
e.label = 'e'
d = e + c
d.label = 'd'
L = d * f
L.label = 'L'

# Manual backpropagation
L.dv = 1 # dL/dL = 1

d.dv = f.v # dL/dd = d/dd(d * f) = f
f.dv = d.v # dL/df = d/df(d * f) = d

c.dv = d.dv # dL/dc = dL/dd * dd/dc = f * d/dc(e + c) = f * 1 = f
e.dv = d.dv # dL/de = dL/dd * dd/de = f * d/de(e + c) = f * 1 = f

a.dv = e.dv * b.v # dL/da = dL/de * de/da = f * d/da(a * b) = f * b
b.dv =  e.dv * a.v # dL/db = dL/de * de/db = f * d/db(a * b) = f * a

L.graph().render('manual_expression', format='pdf', view=True, cleanup=True)

# Automatic backpropagation
L.backward()
L.graph().render('auto_expression', format='pdf', view=True, cleanup=True)
