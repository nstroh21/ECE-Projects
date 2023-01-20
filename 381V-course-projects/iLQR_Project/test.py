from lqr import LQR
import numpy as np
import autograd as ag
from math import sin, cos ,pi

"""
A = np.eye(4)
B = np.eye(4)
Q = np.eye(4)
R = np.eye(4)
this = LQR(A, B, Q, R)
T = 2500
dt = 0.01
this.compute_policy_gains(2500, dt)

alist = [1,2,3,4,5,6]
print(alist[::-1])
print(alist[3:])
print(alist)"""

x = [0,1]
u = np.array([1,1])
f = np.array([2,2])


M=10 
m=80 
g = 9.8
L=1
J=100
gam=.001
c=0.1
dt=.0001
F = 1
Mt = M + m
Jt = J + m*L*L
dx = [0, 0, 0, 0]
x = [0, 0, .5235988, 0]

v, theta, w = x[1], x[2], x[3]   #current velocity, angle, angular velocity
dx[0], dx[2] = v, w

K1 = F - c*v - m*L*sin(theta)*w*w
K2 = m*g*L*sin(theta) - gam*theta
D = (M*Jt) - (m^2)*cos(theta)

vdot = (1/D)*(Jt*K1 + m*L*cos(theta)*K2)
wdot = (1/D)*(K1*m*L*cos(theta) + Mt*K1)

dx[1], dx[3] = vdot, wdot

# to propagate to x_t+1  = x_k + dt*(dx/dt)
jacobian_dyn = ag.jacobian(dx)
jacobian_dyn(np.array(1))

