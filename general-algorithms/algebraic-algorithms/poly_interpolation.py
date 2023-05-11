'''
Polynomial Interpolation.

Created 17/02/23
Developed by Fraser Love
'''

import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return np.tanh(x) ** 2

def g(x):
    return np.tanh(5 * x) ** 2

M = 10 # Number of input points.
xr = (-1, 1) # Range of x values.

# Sampling f(x) over M evenly spaced data points.
x0 = np.linspace(xr[0], xr[1], M)
y0 = f(x0)

# Computing coefficients for Lagrange polynomial fit of f(x) using
# the vandermode matrix (ordered with largest power first).
coeff = np.linalg.solve(np.vander(x0), y0)

N = 100 # Number of evaluation points.
x = np.linspace(xr[0], xr[1], N)

def poly_interp(x, coeff):
    # Evaluation points.
    y = np.zeros_like(x)
    # Calculating exponents.
    exps = (M - 1 - np.arange(M)).reshape(M, 1)
    # Reshaping x for broadcast.
    x = np.reshape(x, (1, np.size(x)))
    # Multiply by coefficients and sum along the right direction.
    return np.sum(np.power(x, exps) * coeff.reshape(M, 1), axis=0)

# Creating two separate plots.
fig, ax = plt.subplots(1, 2, figsize = (16, 5))

ax[0].plot(x, f(x), label = '$f(x)$')
ax[0].plot(x, poly_interp(x, coeff), '.', label = '$p_{10}(x)$')
ax[0].set_xlabel('x')
ax[0].set_ylabel('y')
ax[0].legend()
ax[0].set_title('$p_{9}(x)$ and $f(x)$')

ax[1].plot(x, np.abs(f(x) - poly_interp(x, coeff)))
ax[1].set_xlabel('x')
ax[1].set_ylabel('y')
ax[1].set_title('|$p_{9}(x) - f(x)|$')

plt.show()

# Computing coefficients for Lagrange polynomial fit of g(x) using
# the vandermode matrix (ordered with largest power first).
coeff = np.linalg.solve(np.vander(x0), g(x0))

# Creating two separate plots.
fig, ax = plt.subplots(1, 2, figsize = (16, 5))

ax[0].plot(x, g(x), label = '$g(x)$')
ax[0].plot(x, poly_interp(x, coeff), '.', label = '$p_{9}(x)$')
ax[0].set_xlabel('x')
ax[0].set_ylabel('y')
ax[0].legend()
ax[0].set_title('$p_{9}(x)$ and $g(x)$')

ax[1].plot(x, np.abs(g(x) - poly_interp(x, coeff)))
ax[1].set_xlabel('x')
ax[1].set_ylabel('y')
ax[1].set_title('|$p_{9}(x) - g(x)|$')

plt.show()