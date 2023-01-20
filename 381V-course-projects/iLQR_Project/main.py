import cvxpy as cp
import numpy as np
#import torch 
import autograd as ag
import cart_pole
import lqr

# initial conditions
T = 2500
dt = 0.01
theta0 = .523598776
#theta0 = .17453293
x_init = [0,0, theta0, 0]
problem = cart_pole()

# backward pass to find initial policy

Q = 0.01*np.eye(4)
R = np.eye(2)


# Run Standard LQR Block
A, B = cart_pole.A, cart_pole.B
lqr = lqr.LQR(A,B,Q,R)
K = lqr.compute_policy_gains(T, dt)
x = x_init
#target = theta = pi
X = np.zeros((T, 4), dtype='float64')
U = np.zeros((T), dtype='float64')

for i in range(T):
    u = np.dot(K[i], x)

    # vehicle simulator
    x = np.dot(A, x) + np.dot(B, u)


    X[i, :] = x.transpose()
    U[i, :] = u.transpose()

#iLQR block
costJ = .2

N = 50
xref = np.array([N,4])
xref[0] = x_init
uref = np.ones([N])*.1
# generate nominal trajectory
for i in range(0, N):
    x_next = cart_pole.apply_nonlinear_dynamics(xref[i], uref[i])
    xref[i+1] = x_next
while(costJ > .1): # chose some cost threshold, can tune this
    # choose finite horizon N = 50 
    N = 50
    # backward pass, then forward pass, then check cost and iterate

    # initialize cost matrices
    P = (N+1)*[Q]
    L = (N+1)*[0]
    l = (N+1)*[np.ones(4)]
    Vstar = (N+1)*[0]
    v = (N+1)*0
    H = np.ones(4)
    q = np.ones(4)
    r = 1
    h = 1

    # linearize dynamics
    A_bar, B_bar = cart_pole.linearize_dynamics(xref, uref)
    A = A_bar
    B= B_bar

    #x_delta = np.zeros(50) - 

    # DP Equations & cost calculation
    costJ = (1/2)*np.transpose(xref)
    # did not finish, questioning my calculations for sure
    for i in range(N,0):
        costJ = costJ + Vstar[i+1]

        L[i] = -1*np.linalg.inv(R+np.transpose(B)*P[i+1])(2*np.transpose(B)**P[i+1]*A+H)
        l[i] = -1/2*(np.transpose(r) + q[i+1]*B)
        w = np.transpose(l)*R*l + np.transpose(l)*np.transpose(B)*P[i+1]*B*l + np.transpose(r)*l + h
        v[i] = q[i] + q[i+1] + r[i] + np.transpose(l)*B*H 

        Vstar[i] = np.transpose(x)*K*x + np.transpose(v[i])

        P[i] = P[i]+np.transpose(L[i])*R*L[i] + np.transpose(L[i])*np.transpose(B)*H + np.transpose(A +B*L[i])*P[i]*(A+B*L[i])

    # decision variables are delta x, delta u
    # ? should be multiplying delta not ref but wasnt exactly sure where x delta came from (only know xref?)
    xstar = xref
    udelta = [L[i]*x +l[i]*x]
    ustar = uref + udelta  # if we converge this is the optimal policy
    for i in range(0, N):
        x_next = cart_pole.apply_nonlinear_dynamics(xref[i], ustar[i])
        xstar[i] = x_next

