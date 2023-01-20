from math import pi, sin , cos
import numpy as np
#import sympy, autograd?

class cart_pole(object):
    def __init__(self, M=10, m=80, L=1, J=100, gam=.01, c=0.1):
        #u = actuator force F (will it be constant or [F 0])?, initally policy just set constant 1
        #x = [theta q theta_dot q_dot], intial state = [~10/30 degrees, 0, 0, 0]
        #M, m, L, theta = mass of cart, mass, length, angle of pendulum 
        #g, c, gam, J = physical constants (& J is some bias we put into system) 
        self.M, self.m = M, m
        self.L, self.J= L, J
        self.gam, self.c= gam, c
        self.g = 9.81

    # u is just a scalar for this problem, we can move the cart left and right
    def apply_nonlinear_dynamics(self, x= [0, 0, 0, 0], u = 0, dt =.0001):
        
        # to propagate to x_t+1  = x_k + dt*(dx/dt)
        f = self.f(x, u)
        x_next = x + f*dt

        return  x_next

    # solve for second derviatives, state update as dx/dt (where x is state vector)
    def f(self, x, u):
        
        M, m, J, L, gam, c, g, dt = self.M, self.m, self.J, self.L, self.gam, self.c, self.g, self.dt
        F = u
        M = M + m
        ml, t, q, td, qd = m*L, x[0], x[1], x[2], x[3]
        D =  M*J - (ml*cos(t))**2  
        # Mt = M + m           # for condensing equations
        # Jt = J + m*L*L       # condensing
        funcs = np.array(4)
        funcs[0] = x[3]
        funcs[1] = x[4] 
        funcs[2] = ( -gam*M*td - (ml**2)*sin(t)*cos(t)*(td**2) - c*ml*cos(t)*qd + M*ml*g*sin(t) + F*ml*cos(t) ) / D
        funcs[3] = ( -ml*cos(t)*gam*td - J*ml*sin(t)*(td**2) - J*c*qd + (ml**2)*g*cos(t)*sin(t) + F*J ) / D
        
        return np.array([funcs[0], funcs[1], funcs[2], funcs[3]])

    # linearize about some reference trajectory xref & control uref, generalized so as to be applied in iLQR setting
    def linearize_dynamics(self, xref = np.array([0, 0, 0, 0]), uref = 0):
        # declarations, renaming things for readability
        M, m, J, L, gam, c, g = self.M, self.m, self.J, self.L, self.gam, self.c, self.g
        x,F = xref, uref
        M = M+m
        J = J + (m*L)**2
        t, q, td, qd = x[0], x[1], x[2], x[3]
        # some condensed expressions
        ml = m*L
        D = M*J - (ml*cos(t))**2
        S, C = ml*sin(t) , ml*cos(t)
        K = S*C
        # Gradients: notation: gtf1 = gradient theta of f1 (funcs[2] function), gtd = gradient theta-dot etc.
        gtf1 = ( (-2*K)*(-M*gam*td - K*(td**2) - c*C*qd + M*g*S + F*C))/ (D**2) + ( (-1*(ml*td)**2)*cos(2*t) + c*qd*S + M*g*C - F*S ) / D
        gqf1 = 0
        gtdf1 = (-M*gam - 2*K*td) / D
        gqdf1 = (-c*C)/ D
        
        gtf2 = ((-2*K)*(-C*gam*td - J*S*td**2 - J*c*qd + K*g + F*J) )/(D**2) +  (S*gam*td - J*C*td**2 + (ml**2)*g*cos(2*t)) / D
        gqf2 = 0
        gtdf2 = (-C*gam - 2*J*S*td) / D
        gqdf2 = (-J*c)/D

        guf1 = C/D
        guf2 = J/D

        # Finally, we get our Jacobian matrices:

        Jxf = np.array([[0,    0,    1,     0    ],
                        [0,    0,    0,     1    ],
                        [gtf1, gqf1, gtdf1, gqdf1],
                        [gtf2, gqf2, gtdf2, gqdf2]])  

        Juf = np.array([0, 0, guf1, guf2 ])

        
        return Jxf , Juf
      