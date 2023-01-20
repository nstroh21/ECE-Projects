# Author: Prof. Florian Shkurti, U Toronto CS
# Source: https://github.com/florianshkurti/comp417/blob/master/lqr_examples/python/linear_model_trajectory_following.py
# some comments inserted by Sandeep Chinchali

import scipy
import numpy as np

class LQR(object):
    def __init__(self, A, B, Q, R):
        self.A = A
        self.B = B
        self.Q = Q
        self.R = R


    # Nick Strohmeyer's comments (since we're all putting our last names here)
    # T = total time, dt = step size


    def compute_policy_gains(self, T, dt):
        # Need to stabilize the system around error = 0, command = 0
        
        # create a list of T copies of dynamics matrix, this is here I guess since it might depend on time
        if type(self.A) != type([]):
            self.A = T*[self.A]
            
        # In omnibus example our dynamics our time-independent, but these lines basically generalize to time-dependent dynamics as well
        print(type(self.B) != type([]))
        if type(self.B) != type([]):
            self.B = T*[self.B]


        # initializing P & K , P is terminal cost matrix, K is computed for each step giving us policy gains
        # K should be interpreted as L_i (from Sandeep's slides)
        # P is updated and should be interpreted as K_i (from Sandeep's slide) -- quadratic 
        # V* comes back into equation --> xiPxi --> because we subsitute in dynamics on each step, also makes this unconstrained problem
        self.P = (T+1)*[self.Q]
        self.K = (T+1)*[0]

        for t in range(1, T+1): #T+1

            # this line is actually calculating v* (in a way) it is embedded into the analytical derivation (see lecture 3 notes)
            self.K[t] = np.dot(self.B[T-t].transpose(), np.dot(self.P[t-1], self.A[T-t]))

            F = self.R + np.dot(self.B[T-t].transpose(), np.dot(self.P[t-1], self.B[T-t]))
            F = np.linalg.inv(F)

            self.K[t] = -np.dot(F, self.K[t])  # set the policy at time t --> L_i (linear policy)

            C = self.A[T-t] + np.dot(self.B[T-t], self.K[t])
            E = np.dot(self.K[t].transpose(), np.dot(self.R, self.K[t]))

            # New quadratic cost, propagate this to the next step to calcualte the next K(t)
            self.P[t] = self.Q + E + np.dot(C.transpose(), np.dot(self.P[t-1], C))  


        self.K = self.K[1:]
        self.K = self.K[::-1]  # reverse because first calc was actually for last time step
        self.P = self.P[::-1]  
        return self.K

