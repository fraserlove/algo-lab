'''
Estimating Pi.

Created 28/03/23
Developed by Fraser Love
'''

import numpy as np
import matplotlib.pyplot as plt

def darts(n):
    '''
    Places n points uniformly in the unit square and returns a n x 3 array storing 
    their position and a boolean value describing if they fall within the unit circle.
    
    Parameters:
    n - Integer: number of points
    
    Returns:
    n x 3 array of format [xpos, ypos, inInterior]
    '''
    
    pts = np.random.rand(n, 2)
    dist = np.sqrt(np.sum((pts - 0.5) ** 2, axis=1))
    interior = np.array((dist <= 0.5).astype(int))
    return np.column_stack((pts, interior))


def estimate_pi(pts):
    '''
    Estimates a value of π by the proportion of points which fall inside the unit circle.
    
    Parameters:
    array - n x 3 array of points in format 
    '''
    
    # Area of the unit square is 1 and the area of the unit circle is π / 4.
    # So a proportion of π / 4 points should fall within the circle.
    return 4 * np.mean(pts)


# Estimating π using 'estimate_pi' for increasing values of n
n_values = [50, 100, 1000, 10000]
pi = {n: estimate_pi(darts(n)[:, 2]) for n in n_values}

# ============== Plotting Dart Throwing ==============

# Define figure 4 subplots (2 x 2).
fig, axs = plt.subplots(2, 2, figsize=(10, 10))

for i, n in enumerate(n_values):
    pts = darts(n)
    interior = pts[pts[:, 2] == 1]
    exterior = pts[pts[:, 2] == 0]
    pi = estimate_pi(pts[:, 2])
    
    # Plotting interior and exterior points in blue and red respectively.
    axs[i // 2, i % 2].scatter(interior[:, 0], interior[:, 1], color = 'blue')
    axs[i // 2, i % 2].scatter(exterior[:, 0], exterior[:, 1], color = 'red')
    
    # Setting plot title with n and π estimate.
    axs[i // 2, i % 2].set_title('n = {}, p = {:.4f}'.format(n, pi))
    axs[i // 2, i % 2].set_xlim(0, 1)
    axs[i // 2, i % 2].set_ylim(0, 1)

fig.suptitle(r'Dart Throws for $n \in \{50, 100, 1000, 10000\}$')
plt.show()

# ================= Plotting π vs n =================

n_vals = range(100, 10001, 100)

# Calculate pi estimates for each value of n.
pi = [estimate_pi(darts(n)[:, 2]) for n in n_vals]

# Plot scatterplot of π estimates vs. values of n.
plt.scatter(n_vals, pi)
plt.title('Estimates of π vs. n')
plt.xlabel('n')
plt.ylabel('π estimate')
plt.show()