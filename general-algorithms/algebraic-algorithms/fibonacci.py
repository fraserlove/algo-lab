'''
Fibonacci Sequence Algorithm Comparison

Created 03/02/23
Developed by Fraser Love
'''

from time import process_time
import numpy as np
import matplotlib.pyplot as plt

def Binet(n):
    phi = (1 + np.sqrt(5)) / 2
    psi = (1 - np.sqrt(5)) / 2
    return int((phi ** n - psi ** n) / np.sqrt(5))

def fibIter(n):
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b # Calculating the i-th fibonacci term
    return a

def fibMatP(n):
    mat = np.array([[1, 1], [1, 0]])
    return np.linalg.matrix_power(mat, n)[0][1] # Computing [[1, 1], [1, 0]]^n

fig, ax = plt.subplots()

funcs = (Binet, fibIter, fibMatP)
iters = 50 # Number of iterations per n
nran = np.arange(400, 1400 + 1, 10) #NumPy array storing values of n in range [400, 1400]

# Calculates the time taken to perform n iterations of the fibonacci sequence, for increasing n
def time_func(func):
    elapsed = np.zeros(len(nran)) # Array to store elapsed time
    for i, n in enumerate(nran):
        start = process_time()
        for _ in range(iters): # Repeat a total of iters times to get a consistent measure
            func(n)
        stop = process_time()
        elapsed[i] = stop - start
    return elapsed

for func in funcs: # Plot each function
    plt.plot(nran, time_func(func), label = func.__name__)

ax.set_xlabel('Number of Iterations ($n$)')
ax.set_ylabel('Compute Time ($s$)')
plt.legend()
plt.show()