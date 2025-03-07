from autodiff import Value

# Inputs x1, x2
x1 = Value(2.0, label='x1')
x2 = Value(0.0, label='x2')

# Weights w1, w2
w1 = Value(-3.0, label='w1')
w2 = Value(1.0, label='w2')

# Bias
b = Value(6.8813735870195432, label='b')

# o = tanh(x1 * w1 + x2 * w2 + b)
x1w1 = x1 * w1
x1w1.label = 'x1 * w1'
x2w2 = x2 * w2
x2w2.label = 'x2 * w2'
x1w1x2w2 = x1w1 + x2w2
x1w1x2w2.label = 'x1 * w1 + x2 * w2'
z = x1w1x2w2 + b
z.label = 'z'
o = z.tanh()
o.label = 'o'

# Manual backpropagation
o.dv = 1

# do/dz = d(tanh(z))/dz = 1 - tanh(z)^2 = 1 - o^2
z.dv = 1 - o.v**2  

# do/d(x1w1x2w2) = do/dz * dz/d(x1w1x2w2) = do/dz * 1 = do/dz
x1w1x2w2.dv = z.dv  

# do/db = do/dz * dz/db = do/dz * 1 = do/dz
b.dv = z.dv  

# do/d(x1w1) = do/d(x1w1x2w2) * d(x1w1x2w2)/d(x1w1) = do/d(x1w1x2w2) * 1
x1w1.dv = x1w1x2w2.dv  

# do/d(x2w2) = do/d(x1w1x2w2) * d(x1w1x2w2)/d(x2w2) = do/d(x1w1x2w2) * 1
x2w2.dv = x1w1x2w2.dv  

# do/dx1 = do/d(x1w1) * d(x1w1)/dx1 = do/d(x1w1) * w1
x1.dv = x1w1.dv * w1.v  

# do/dw1 = do/d(x1w1) * d(x1w1)/dw1 = do/d(x1w1) * x1
w1.dv = x1w1.dv * x1.v  

# do/dx2 = do/d(x2w2) * d(x2w2)/dx2 = do/d(x2w2) * w2
x2.dv = x2w2.dv * w2.v  

# do/dw2 = do/d(x2w2) * d(x2w2)/dw2 = do/d(x2w2) * x2
w2.dv = x2w2.dv * x2.v  
o.graph().render('manual_neuron', format='pdf', view=True, cleanup=True)

# Automatic backpropagation
o.backward()
o.graph().render('auto_neuron', format='pdf', view=True, cleanup=True)
