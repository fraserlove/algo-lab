import os
import numpy as np
from matplotlib import rc
import matplotlib.pyplot as plt

'''
Creates a bifurcation diagram for the logistic map and saves it as 'bifurcation.png' under the scripts parent directory.
'''

# Use LaTeX serif font for labels.
rc('font', **{'family': 'serif', 'serif': ['Computer Modern'], 'size': 16})
rc('text', usetex=True)

dpi = 1000 # Figure DPI

class AnnotatedFunction:
    ''' A callable class representing a mathematical function and its LaTeX representation. '''

    def __init__(self, func, label):
        self.func = func
        self.label = label

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


def bifurcation(f: AnnotatedFunction, r0: float, r1: float, x0: float, N: int, M: int) -> None:
    '''
    Plots a bifurcation diagram (i.e. plots x against r) for the map f.
    
    :param f: An AnnotatedFunction describing a map. It takes the current value of x and returns f(x).
    :param r0: Starting value of the parameter r.
    :param r1: Final value of the parameter r.
    :param x0: Initial value of x.
    :param N: Number of iterations or steps to perform for each value of r.
    :param M: Number of iterations to use in plotting the bifurcation diagram.
    '''

    plt.figure(figsize=(18, 8), dpi=dpi)

    r = np.linspace(r0, r1, N)
    pts = np.empty((N - M, 2))

    x = x0 * np.ones(N)
    for i in range(N):
        x = f(r, x)
        if i >= N - M:
            plt.plot(r, x, ',k', alpha=0.2)

    plt.xlim(r0, r1)
    plt.xlabel('$r$')                               
    plt.ylabel('$x$')   
    plt.title(f'$F_r(x) = {f.label}$')
    img_path = f'{os.path.dirname(os.path.abspath(__file__))}/bifurcation.png'
    plt.savefig(img_path, dpi=dpi, bbox_inches='tight')


if __name__ == '__main__':
    logistic_map = lambda r, x: r * x * (1-x)
    f = AnnotatedFunction(logistic_map, 'rx(1-x)')

    bifurcation(f, r0=2.8, r1=4.0, x0=0.1, N=100000, M=1000)