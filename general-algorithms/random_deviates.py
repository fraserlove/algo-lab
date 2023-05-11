'''
Box-Muller, Larsen and Marx, and Mood, Graybill and Boes methods.

Created 24/03/23
Developed by Fraser Love
'''

import numpy as np

def rbmdev(seed, n):
    '''
    Generates an array of n random deviates from a normal distribution with mean value 
    zero and standard deviation one using the Box-Muller method.

    Parameters:
    seed - int (seed for the random number generator).
    n - int (number of deviates to generate).

    Returns:
    Array of shape (n,) (array of n random deviates with mean zero and standard deviation one).
    '''
    
    rng = np.random.default_rng(seed)
    A = rng.uniform(size = (n + 1) // 2)
    B = rng.uniform(size = (n + 1) // 2)
    
    x1 = np.sin(2.0 * np.pi * A) * np.sqrt(-2 * np.log(B))
    x2 = np.cos(2.0 * np.pi * A) * np.sqrt(-2 * np.log(B))
    return np.concatenate([x1, x2])[:n]


def rlmdev(seed, n, m):
    '''
    Generates an array of n random deviates from a chi-squared distribution with 
    m degrees of freedom using the Larsen and Marx method.

    Parameters:
    seed - int (seed for the random number generator).
    n - int (number of deviates to generate).
    m - int (number of degrees of freedom).

    Returns:
    Array of shape (n, m) (n random deviates from a chi-squared distribution with m degrees of freedom).
    '''
    
    x = rbmdev(seed, n * m).reshape((n, m))
    return np.sum(x ** 2, axis = 1)


def rmgbdev(seed, n, m):
    '''
    Generates an array of n random deviates from a Student-t distribution with 
    m degrees of freedom using the Mood, Graybill and Boes method.

    Parameters:
    seed - int (seed for the random number generator).
    n - int (number of deviates to generate).
    m - int (number of degrees of freedom).

    Returns:
    Array of shape (n, m) (n random deviates from a Student-t distribution with m degrees of freedom).
    '''
    
    z = rbmdev(seed, n)
    u = rlmdev(seed, n, m)
    return z / np.sqrt(u / m)