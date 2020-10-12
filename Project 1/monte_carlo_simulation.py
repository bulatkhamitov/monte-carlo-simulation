import random
import math

def tri_sample(A, B, C):
    """ Return the point sampled uniformly in the triangle ABC. """
    r1 = random.random()
    r2 = random.random()
    
    s1 = math.sqrt(r1)
    
    x = A[0] * (1.0 - s1) + B[0] * (1.0 - r2) * s1 + C[0] * r2 * s1
    y = A[1] * (1.0 - s1) + B[1] * (1.0 - r2) * s1 + C[1] * r2 * s1
    
    return (x, y)

def sign(x):
    """ Return the sign of a finite number x. """
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0    

def ccw(A, B, C):
    """ Return 1 if A-B-C is a counterclockwise turn, 
              -1 for clockwise,
               0 if the points are collinear (or not all distinct). """
    disc = (A[0] - C[0]) * (B[1] - C[1]) - (A[1] - C[1]) * (B[0] - C[0])
    return sign(disc)

def classify_points(A, B, C, D):
    """ Return 1 if a convex hull of A, B, C and D is a quadrilateral,
              -1 if a triangle,
               0 if any three of A, B, C and D are collinear (or if not all points are distinct). """
    return ccw(A, B, C) * ccw(A, B, D) * ccw(A, C, D) * ccw(B, C, D)

def monte_carlo_simulation(N):
    A = (0, 0)
    B = (0.5, math.sqrt(.75))
    C = (1, 0)
    
    points = []
    quad_points = []    
    results = []        
          
    points = [tri_sample(A, B, C) for _ in range(N)] 
    
    quad_counter = 0
    total_counter = 0
    
    for _ in range(1, N + 1):
        quad_points = random.sample(points, 4)

        A = quad_points[0]
        B = quad_points[1]
        C = quad_points[2]
        D = quad_points[3]
    
        classify_points(A, B, C, D)
        
        total_counter += 1    
        
        if classify_points(A, B, C, D) == 1:
            quad_counter += 1 
            
        results.append(quad_counter / total_counter)
    return results

results = monte_carlo_simulation(10000)

import numpy as np
import matplotlib.pyplot as plt

XX = np.linspace(1, 10000, 10000)
YY = results

plt.figure(figsize=(8, 4))
plt.scatter(XX, YY, s=0.3, color="blue", label="Monte-Carlo simulation")
plt.hlines(2/3, 100, 10000, colors="red", label="Analytical solution")
plt.ylim(0.6, 0.8)
plt.xlabel("$N$")
plt.ylabel("$P$")
plt.legend()
# plt.savefig('result.pdf')
plt.show()
