import cvxpy as cvx
import numpy as np
import matplotlib.pyplot as plt

##### Problem Overview #####
# State s: = (x,y, theta, x_dot, y_dot, th_dot)
# Reference Point:  (1,0 ,0, 0, 0, 0)
# MPC :  run 2 experiments:  40 and 150 time steps for the prediction horizon

# simplified propulsion jet model, linearized dynamics given below by A
g, c, m , r, J = 9.8, .05, 4, 0.25, 0.475

A = np.array(
    [[ 0, 0,   0,  1,    0,    0 ],
     [ 0, 0,   0,  0,    1,    0 ],
     [ 0, 0,   0,  0,    0,    1 ], 
     [ 0, 0,  -g, -c/m,  0,    0 ], 
     [ 0, 0,   0,  0,   -c/m,  0 ],
     [ 0, 0,   0,  0,    0,    0 ]] )

B = np.array(
    [[ 0,    0   ],
     [ 0,    0   ],
     [ 0,    0   ], 
     [ 1/m,  0   ], 
     [ 0,    1/m ], 
     [ r/J,  0   ]])

Q, R = np.eye(6), np.eye(2)
s0 = [0,0,0,0,0,0]
S, Pi = [s0],  []


def optimize(s, s_ref, T, u0 = [.1,.1]):

    X, U, DX, DU = {}, {}, {}, {}  
    cost_terms,  constraints = [] , []  
    s0 = np.array(s) 
    u0 = np.array(u0)  # previous control
    sN = np.array(s_ref) # target state
    tau = 0

    for tau in range(T):

        X[tau] = cvx.Variable(6) 
        U[tau] = cvx.Variable(2) 
        DX[tau] = sN - cvx.Variable(6) # Delta X
        if tau == 0:
            DU[tau] = U[tau] - u0  # Delta U
        else:
            DU[tau] = U[tau] - U[tau-1]
        
        cost_terms.append( cvx.quad_form(DX[tau],Q) ) # state cost
        cost_terms.append( cvx.quad_form(DU[tau],R) ) # control cost

        if tau == 0:
            constraints.append(X[tau] == s0)
        else:
            constraints.append(  0.1*(A @ X[tau-1] + B @ U[tau-1]) + X[tau-1] ==  X[tau] ) 
            constraints.append(U[tau] == U[tau-1] + DU[tau])
            constraints.append(X[tau] - sN == DX[tau])
        
        # Box constraints 
        constraints.append(cvx.norm(U[tau], "inf") <= 0.3)
        constraints.append(cvx.norm(U[tau] + DU[tau], "inf") <= 0.3)
    
    # Solve
    objective = cvx.sum(cost_terms)
    problem = cvx.Problem(cvx.Minimize(objective), constraints)
    problem.solve()
    # print(problem.status)
    if problem.status == "infeasible":
        return None
    else:
        return U[0].value + DU[0].value   # return 1st step from sequence
    

def sim_step(s, pi, Ts = 0.1):
    # dynamics: s[k+1] = Ts(s_dot) + s[k] ... where s_dot = As + Bu
    pi = np.array(pi)
    s_dot = np.dot(A,s) +  np.dot(B,pi)
    new = Ts*s_dot + s 
    S.append(list(new))
    return

def main():
    measure_horizon = 200
    control_horizon = 20
    target = [1, 1, 0, 0, 0, 0]
    t, u0 = 0, []
    while t < measure_horizon:
        s = S[t]  # current state measurement

        # tracking problem/ update reference as we go -- mess around here
        """if t % 10 == 0:
            command = np.random.randn()
            if t % 20 == 0:
                target = [command, 1+command, 0, 0, 0, 0]
            else:
                target = [command, 1-command, 0, 0, 0, 0] """

        if t == 0:
            u0 = [.05, .05]  # impulse to system
        else:
            u0 = Pi[t-1]
        U_star = optimize(s, target, control_horizon, u0) 
        if U_star is None:
            print("Problem is Infeasible at Step:", t)
            break
        else:
            pi = list(U_star)
            Pi.append(pi)
            sim_step(s, pi)
        t += 1
    return t

t = main()

print("done")
# plot results:
x_coord, y_coord, thetas = [], [], []
F1 = []
F2 = []
steps = np.arange(0,t+1,1)
for state in S:
    x_coord.append(state[0])
    y_coord.append(state[1])
    thetas.append(state[2])
for action in Pi:
    F1.append(action[0])
    F2.append(action[1])

fig, ax = plt.subplots(1, 2)

ax[0].plot(steps, x_coord)
ax[0].set_title('X position over time')

#ax1.title('X position over time')
ax[1].plot(steps, y_coord, color = 'r')
ax[1].set_title('Y position over time')

plt.show()

plt.clf()

fig, ax = plt.subplots(1, 2)
ax[0].plot(steps[0:t], F1, color = 'g')
ax[0].set_title('F1 Over Time')

ax[1].plot(steps[0:t], F2)
ax[1].set_title('F2 Over Time')
plt.show()

plt.clf()

plt.scatter(x_coord, y_coord)
plt.title("States Visited(x,y)")
plt.show()

plt.plot(steps, thetas, color = 'c')
plt.title('Theta Over Time Steps')
plt.show()
# another way to do this plotting simply 
    # define subplots
    # fig, ax = plt.subplots(2, 2)
