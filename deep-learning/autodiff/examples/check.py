import numpy as np
from autodiff import Value

def finite_difference_gradient(f: callable, x: Value, eps: float = 1e-8) -> np.ndarray:
    """Estimates the gradient of a function using the central difference formula."""
    return (f(x + eps) - f(x - eps)) / (2 * eps)

x = Value(2)
f = lambda x: (-(x**2).sin() + 5).exp()
y = f(x)
y.backward()
y.graph().render('check', format='pdf', view=True, cleanup=True)


assert np.isclose(finite_difference_gradient(f, x).v, x.dv, atol=1e-4)

print('Gradient check passed')