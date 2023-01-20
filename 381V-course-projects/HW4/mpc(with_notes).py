import cvxpy as cvx
import numpy as np
import matplotlib.pyplot as plt

##### Problem Overview #####
# State Definition:
    # s = (x,y, theta, x_dot, y_dot, th_dot)
# Reference Point:
    # (1,0 ,0, 0, 0, 0)
# MPC : pi[k] is derived from optimizing over finite control horizon
    # returns a list of controls, from which we will only apply the first (current state-action)
    # aquire x[k+1] and then re-run the optimization problmem, shifting the horizon by 1 sample
# run 2 experiments:  40 and 150 time steps for the prediction horizon


# simplified propulsion jet model, linearized dynamics given below by A
g, c, m , r, J = 9.8, .05, 4, 0.25, 0.475

term_weight = 2   # optional parameter: determines how aggressively to penalize deviation from terminal (same for each state)
term_wts = np.array([1,1,1,1,1,1]) # weight by specific state

A = [[ 0, 0,   0,  1,    0,    0 ],
     [ 0, 0,   0,  0,    1,    0 ],
     [ 0, 0,   0,  0,    0,    1 ], 
     [ 0, 0,  -g, -c/m,  0,    0 ], 
     [ 0, 0,   0,  0,   -c/m,  0 ],
     [ 0, 0,   0,  0,    0,    0 ]]

A = np.array(A)  # better for cvxpy

B = [[ 0,    0   ],
     [ 0,    0   ],
     [ 0,    0   ], 
     [ 1/m,  0   ], 
     [ 0,    1/m ], 
     [ r/J,  0   ]]

B = np.array(B)

Q = np.eye(6)
R = np.eye(2)
P = term_weight * np.eye(6)

# init list of states ( initial state)
s0 = [0,0,0,0,0,0]
S = [s0]
Pi = []

term_weight = 2   # determines how aggressively to penalize deviation
                    # from the terminal cost (right now just weighting states equally)
P = term_weight * np.eye(6)

def optimize(s, s_ref, T, u0 = [.1,.1]):
    # function receives current state, reference --> optimize for the control horizon T using cvxpy
    # constraints are dynamics & box constraints on F1 , F2 
    X, U, DX, DU = {}, {}, {}, {}  # dictionaries of states, controls, deltas

    cost_terms,  constraints = [] , []  
    s0 = np.array(s)  # cvxpy can recognize an np array so this is fine
    u0 = np.array(u0) # previous control so we can calc delta_u on 0th time step
    #print(u0)
    sN = np.array(s_ref) # target terminal state
    tau = 0
    # define our cost, iterative building, referencing tracking so we need variables for deltas
    for tau in range(T):

        X[tau] = cvx.Variable(6) # state variable for time t -- 6 states
        U[tau] = cvx.Variable(2) # control variable for time t -- 2 control inputs
        DX[tau] = sN - cvx.Variable(6)  # delta of our state variable versus reference trajectory
        if tau == 0:
            DU[tau] = U[tau] - u0  # delta controls always looks back 1 time step
        else:
            DU[tau] = U[tau] - U[tau-1]
        
        # cost is terms of deltas
        cost_terms.append( cvx.quad_form(DX[tau],Q) ) # state cost
        cost_terms.append( cvx.quad_form(DU[tau],R) ) # control cost
        # cost_terms.append(cvx.quad_form(DX[tau], P)) # this term goes away in reference tracking

        # constraints on initial state & dynamics at all future time steps
        if tau == 0:
            constraints.append(X[tau] == s0)
        else:
            constraints.append(  0.1*(A @ X[tau-1] + B @ U[tau-1]) + X[tau-1] ==  X[tau] )   # put discretized dynamics into constraints
            constraints.append(U[tau] == U[tau-1] + DU[tau])
            constraints.append(X[tau] - sN == DX[tau])
        # Box constraints are the same for all time steps
        constraints.append(cvx.norm(U[tau], "inf") <= 0.3)
        # Box constraint for delta as well ?
        constraints.append(cvx.norm(U[tau] + DU[tau], "inf") <= 0.3)
        
        
        # Add constraint to get delta in there ? 
        #constraints.append(sN - X[tau] == DX[tau])
    
    objective = cvx.sum(cost_terms)
    problem = cvx.Problem(cvx.Minimize(objective), constraints)
    problem.solve()
    #print(problem.status)
    if problem.status == "infeasible":
        return None
    else:
        return U[0].value + DU[0].value   # only return the first control from the opt sequence
    

def sim_step(s, pi, Ts = 0.1):
    # system evolves as:   s[k+1] = Ts(s_dot) + s[k] ... where s_dot = As + Bu
    pi = np.array(pi)
    s_dot = np.dot(A,s) +  np.dot(B,pi)
    new = Ts*s_dot + s 
    S.append(list(new))
    return

def main():
    # outline
    # init some things   Q, A, B, S (or could just leave them up in the header of the file)
    measure_horizon = 400
    control_horizon = 150
    target = [1, 1, 0, 0, 0, 0]
    P = term_weight * np.eye(6)
    t, u0 = 0, []
    while t < measure_horizon:
        s = S[t]  # current state measurement
        if t == 0:
            u0 = [.05, .05]  # impulse to system
        elif t > 0:
            u0 = Pi[t-1]
        else:
            pass
        
        U_star = optimize(s, target, control_horizon, u0)  #remember optimize returns a delta action

        if U_star is None:
            print("Problem is Infeasible at Step:", t)
            break
        else:
            if type(U_star) != None:
                pi = list(U_star)
                Pi.append(pi)
                sim_step(s, pi)
        t += 1
    return t

t = main()  #runs MPC 
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
# another way to do this plotting simply ?
    # define subplots
    # fig, ax = plt.subplots(2, 2)
