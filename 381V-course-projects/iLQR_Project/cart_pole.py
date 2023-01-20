from math import pi, sin , cos
import numpy as np
import lqr as lqr
import sympy as sym
import autograd as ag


class cart_pole():

    def __init__(self, M=10, m=80, L=1, J=100, gam=.001, c=0.1, dt=.0001):
        
         #u = actuator force F (will it be constant or [F 0])?, initally policy just set constant 1
        #x = [q qdot theta thetadot], intial state = [0, 0, 10/30 degrees, 0]
        #M, m, L, theta = mass of cart, mass, length, angle of pendulum 
        #g, c, gam, J = physical constants (& J is some bias we put into system) 
        self.M, self.m = M, m
        self.L, self.J= L, J
        self.gam, self.c= gam, c
        self.dt = dt
        self.g = 9.81

        # linearized matrices around fixed point 0,0
        # I did not solve these using Jt & pendulum damping, need to update
        A = np.array([[0,   1,                         0,  0], 
                      [0, -c/M,            -1*m*self.g/M,  0],
                      [0,    0,                        1,  0],
                      [0, c/(M*L), (1*(m+M)*self.g)/(M*L), 0] ])
        
        BT = np.array([0, 1/M, 0, -1/(M*L)])
        B = np.transpose(B)

        #Q = 0
        #R = 0
        

    # u is just a scalar for this problem, we can move the cart left and right
    def apply_nonlinear_dynamics(self, x= [0, 0, .5235988, 0], u = 1, dt =.001):
        
        # to propagate to x_t+1  = x_k + dt*(dx/dt)
        f = self.f(x, u)
        x_next = x + f*dt

        return  x_next

    def f(self, x,u):
        
        M, m, J, L, gam, c, g, dt = self.M, self.m, self.J, self.L, self.gam, self.c, self.g, self.dt
        F = u
        Mt = M + m
        Jt = J + m*L*L
        funcs = np.array(4)
        funcs[0] = x[1]
        funcs[1] = ( 1/(M*Jt - (m**2)*cos(x[2])) )*(Jt*(F - c*x[1] - m*L*sin(x[2])*x[3]*x[3]) + m*L*cos(x[2])(*m*g*L*sin(x[2]) - gam*x[2]))
        funcs[2] = x[3]
        funcs[3] = ( 1/(M*Jt - (m**2)*cos(x[2])) )*((F - c*x[1] - m*L*sin(x[2])*x[3]*x[3])*m*L*cos(x[2]) + Mt* (m*g*L*sin(x[2]) - gam*x[2]) )

        return np.array([funcs[0], funcs[1], funcs[2], funcs[3]])

    def linearize_dynamics(self, xref = np.array([0, 0, 0, 0]), uref = 1):
        
        M, m, J, L, gam, c, g, dt = self.M, self.m, self.J, self.L, self.gam, self.c, self.g, self.dt
        Mt = M + m
        Jt = J + m*L*L
        D = (M*Jt) - (m^2)*cos(xref[2])
        f =self.f(xref,uref)

        #jacobians , wasn't quite figure out how to code this part, put these out in main
        Jx = ag.jacobian(f)(xref)
        Ju = ag.jacobian(f)(uref)

        # using jacobians, formulas for A,B are:

        
        return Jx
      







# scratch dynamics, simplified dynamics above

""" 
      M, m, J, L, gam, c, g, dt = self.M, self.m, self.J, self.L, self.gam, self.c, self.g, self.dt
        F = u
        Mt = M + m
        Jt = J + m*L*L
        dx = [0, 0, 0, 0]

        v, theta, w = x[1], x[2], x[3]   #current velocity, angle, angular velocity
        dx[0], dx[2] = v, w

        K1 = F - c*v - m*L*sin(theta)*w*w
        K2 = m*g*L*sin(theta) - gam*theta
        D = (M*Jt) - (m^2)*cos(theta)

        vdot = (1/D)*(Jt*K1 + m*L*cos(theta)*K2)
        wdot = (1/D)*(K1*m*L*cos(theta) + Mt*K2)

        dx[1], dx[3] = vdot, wdot   """
