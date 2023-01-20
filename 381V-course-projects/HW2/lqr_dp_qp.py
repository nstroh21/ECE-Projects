# based on course notes ECE 381V, Prof. Sandeep Chinchali, Fall 2022, course website:

import cvxpy as cp
import numpy as np
from cart_pole import cart_pole 
from matplotlib import pyplot as plt
from lqr import LQR
#import math

# Instantiate cart pole with same parameters as HW 1 & dynamics at 0 point
cart = cart_pole()
Ts = 1/10000   # sample rate
T = 500      # time horizon
I =  np.eye(4)
Q, R = I, .01
S = np.array([1, 0, 0, 0])
A, B = cart.linearize_dynamics(xref=[0, 0, 0, 0], uref = 0)
A, B = I + Ts*A , Ts*B
# discrete linearized dynamics :  x_k+1 = Ax_k + Bu_k

#x_init = np.array([2, 0, 0, 0])            #test random points
# x_init = np.array([.174532925, 0, 0, 0])   # theta is 10 degrees offset
x_init = np.array([.523598776, 0, 0, 0])    # theta is 30 degrees offset

x = x_init
X = np.zeros((T,4), dtype ='float64')
U = np.zeros((T,1), dtype ='float64')

# Finding a policy using DP equations
lqr = LQR(A, B, Q, R)
K = lqr.compute_policy_gains(T, Ts)

# simulate:
for i in range(T):
    u = np.dot(K[i], x)
    
    # This is essentially the simulator of cart
    x = np.dot(A, x) + np.dot(B, u)
    X[i, :] = x.transpose()
    U[i, :] = u.transpose()

# """

########### PART 2: As a quadratic program in cvxpy #################
""" 
T = 100    #overwrite T with soemthing smaller
# initialize for cvxpy: (X, U already defined)
X = {}
U = {}
cost_terms = []
constraints = []

# use iterative builidng solution from notes
for t in range(T):
    X[t] = cp.Variable(4)
    U[t] = cp.Variable()
    cost_terms.append(cp.quad_form(X[t], Q))
    cost_terms.append(U[t]*R)
    #print(U[t]*R)
    #print(cp.quad_form(X[t], Q).value)
    #cost_terms.append(X[t] @ (S * U[t]) )

    if (t == 0):
        constraints.append( X[t] == x_init )
    if (t < T-1 and t > 0):
        constraints.append(A @ X[t-1] + B * U[t-1] == X[t])


objective = cp.Minimize(cp.sum(cost_terms))
problem = cp.Problem(objective, constraints)
problem.solve()
print(problem.status)
print(problem.value)
print(U[0].value) # optimal control sequence

# outputs X and U as sequences, recover entire list as:
X = X[0]
U = U[0] 

"""

# PLOTS : can be used for either part a or part b

# States, plot 
plt.figure()
plt.plot( X[:, 0], '-b')
plt.plot( X[:, 1], '-r')
plt.plot( X[:, 2], '-g')
plt.plot( X[:, 3], '-k')
plt.legend(['theta', 'q', 'theta_dot', 'q_dot'])
plt.xlabel('time steps')
plt.title('Init Theta = 30deg, DP Solution')
plt.show()


# Controls, plot 
plt.figure()
plt.plot( U[:, 0], '-b')
plt.legend(['Control: F_cart'])
plt.xlabel('time steps')
plt.show()

