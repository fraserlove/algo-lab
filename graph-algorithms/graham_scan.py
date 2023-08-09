'''
Graham Scan Algorithm for Computing the Convex Hull.

Created 10/02/23
Developed by Fraser Love
'''

import numpy as np
import matplotlib.pyplot as plt

#===============================================================
# Returns the cross product between 3 points.
# p1, p2, p3 - 2 x 1 arrays describing the points
#===============================================================
def cross_prod(p1, p2, p3):
    return np.cross((p1 - p2), (p3 - p2))


#===============================================================
# Returns the inverse gradient between two points.
# p1, p2 - 2 x 1 arrays describing the points
#===============================================================
def inv_grad(p1, p2):
    if np.array_equal(p1, p2):
        return np.inf # Removes possibility of division by zero.
    return (p1[0] - p2[0]) / (p1[1] - p2[1])


#==============================================================
# Returns a sorted array of indices describing the angle
# between each point and a chosen point.
# pts - array storing gradient values
# pt - chosen point to find angles from
#==============================================================
def sort_grads(pts, pt):
    inv_grads = [inv_grad(pts[i], pt) for i in range(pts.shape[0])]
    # Sorting indices of inverse arguments.
    return np.argsort(np.array(inv_grads))


#==============================================================
# Computes and returns the convex hull of size 2 x m from a set 
# of 2 x n points using the Graham scan algorithm.
# pts - a 2 x n array of points
#==============================================================
def get_hull(pts):
    # Transposing points into a total of n, (x, y) pairs.
    pts = np.transpose(pts)
    # Point with minimium y-coord.
    p1 = pts[np.argmin(pts, axis = 0)[1]]
    # Point with maximum inverse gradient from min y-coord.
    p2 = pts[sort_grads(pts, p1)[0]]
    # Initialing the hull with points of min y coord and max inverse grad.
    hull = np.array([p1, p2])
    
    # Iterating over sorted points, except start point (which is p2) and last point (which is p1).
    for point in sort_grads(pts, p1)[1:-1]:
        # Appending next point to end of the hull.
        hull = np.vstack([hull, pts[point]])

        # Check for concavity of hull. - i.e. check that cross product (angle) between
        # three last points in the hull is negative (indicating left turn).
        while (cross_prod(*hull[-3:])) < 0:
            # If true, need to replace penultimate point.
            hull = np.delete(hull, -2, axis=0)
            
    # Transposing to return a 2 x m array describing the hull.
    return np.transpose(hull)

N = 40

points = np.random.rand(2,N)
hull = get_hull(points)

plt.plot(points[0,:],points[1,:],'.')
plt.plot(np.append(hull[0,:],hull[0,0]),np.append(hull[1,:],hull[1,0]))
plt.show()