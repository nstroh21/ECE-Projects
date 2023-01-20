import torch
from math import pi, sin , cos
import numpy as np
import lqr as lqr
import autograd as ag

# may generalize later, for now, follow github and put all relevant functions here

def ilqr():

    def __init__(self, n=100, max_iter = 150, **kwargs):
        """
        n is the length of the control sequence
        max_iter is the limit of optimization iterations"""

        self.target = [pi/2] # pole is upright ... something like this come back later
        self.max_iter = max_iter
        self.epislon = .001  # seems fine to use ?
        self.n = n

    
    def apply_dynamics(self, x, u, dt):   # apply nonlinear step-by-step, timestep needed?
        " x is vector for current state, u is a vector for current control"
        " found some cart-pole equations online, no idea if this is correct exactly"
        " u is a scalar in this system"
        
        # expect state:  [x, theta, x', theta']
        # expect u to be: [action, 0]

        l = 1   # length of pole
        mc = 1  # mass of cart
        mp = 1  # mass of pole
        M = mc+mp
        g = 9.81 
        theta = x[1]
        thetadot = x[3]

        # nonlinear dynamics I found online # dd = "double-dot"
        xdd = (u[0] + [mp*sin(theta)*( l*thetadot**2 + g*cos(theta) )]) /  (mc +mp*(sin(theta)**2))
        thetadd = ( - u[0]*cos(theta) - mp*l*(thetadot**2)*cos(theta)*sin(theta) - M*g*sin(theta)  ) / (l*(mc + mp*sin(theta)**2))
        
        new_state = x + [xdd*dt**2, thetadd*dt**2, xdd*dt, theta*dt]  # i'm not sure how else to calculate this right now

        return new_state
    
    def linearize_dynamics(f, x, u):   
        """f is function of x & u, A = jacobian wrt x, B = jacobian wrt to u 
            nominal so use xbar, ubar """
        return (ag.jacobian(f, x), ag.jacobian(f, u))
    
    def quadratize_cost():

        """ C is going to calculated experimentally, that is we just find in
            the forward pass step --> c(x, u)"""

        # qk = C_x(xbar,ubar)
        # rk = C_u(xbar, ubar)
        # Qk = C_xx(xbar, ubar)
        # Rk = C_uu(xbar, ubar)
        # Hk = C_xu (xbar, ubar)
        qk = 1
        rk = 1
        Qk = 1
        Rk = 1
        Hk = 1

        "need to use some variant of LQR code to implement DP optimization step"

        return qk , rk , Qk, Rk, Hk

    # linearized dynamics arrays : f_x + f_u = Ax + Bu
    fx = np.zeros(1)
    fu = np.zeros(1) 

    def forward_pass(self, x_o, u_star, n):
        steps = n
        new_state = np.zeros([steps,4])
        new_state[0:] = x_o
        for i in range(1,steps):
            new_state[i:] = self.applydynamics(new_state[i-1:], u_star[i-1], .001) # idk some small time step?

        return new_state
    
    def backward_pass(self):
        cost = 1
        return cost
    

    def main(self, x_o , xbar=None, ubar=None):

        if (ubar == None):
            ubar = 0
        
        xbar = self.forward_pass(x_o, ubar)
        old_cost = get_cost
        ubar_star = 1 #backwardpass
        new_cost = get_cost(xbar,ubar_star)
        if new_cost < old_cost:
            continue
        if new_cost < self.epsilon:
            return ubar
    
        " Shit I have no idea what the fuck im doing :(((( "

        



