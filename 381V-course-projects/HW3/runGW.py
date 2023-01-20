from gridworld import gridworld 
import numpy as np
import matplotlib.pyplot as plt

# Init World/ Globals
setgoal = (19,9)
setinit = (19,19)

world = gridworld(start = setinit, goal = setgoal)
size = world.size
initial = world.start
print(initial)
goal = world.goal

# Value Iteration Algorithm
def valueIteration():
    curr = [[ 0 for i in range(20)] for j in range(20)]
    prev = [[0 for i in range(20)] for j in range(20)]
    iters , i= 0,  0
    while iters < 1000:
        # calcualte values for all states
        for i in range(size):
            for j in range(size):
                world.state = (i,j) # increment state
                if world.state == goal:
                    val = world.computeValues(prev)
                else:
                    val = max(world.computeValues(prev)) # update value , make sure this didnt break
                curr[i][j] = round(val,2)
                #print(curr[i][j])
        # check convergence
        if iters != 1:
            delta = world.checkStop(curr, prev)
            # condition is to be small 10x in a row?
            if(delta < .001):
                    print("State Space Sweeps to Converge:", iters)
                    break
        # update prevValues to currValues
        for i in range(size):
            for j in range(size):
                prev[i][j] = curr[i][j]
        iters += 1
    return curr

# policy evaluation , subroutine of policy iteration
def policyEvaluation(pi, currVal): 
    delta, iters = 0, 0
    while (delta < .01) and iters < 1000:
        for i in range(0,size):
            for j in range(0,size):
                world.state = (i,j)
                a = pi[i][j]  
                n = world.getNeighbors()
                v = currVal[i][j]
                currVal[i][j] = world.computePolicyStep(move = a, values = currVal, nbrs = n)
                delta = max(delta, abs(currVal[i][j] - v))
        iters += 1
    return currVal

#  Policy Iteration Algorithm:
def policyIteration():
    #V = value function to converge to optimal, Pi to converge on best policy
    empty = [[0 for i in range(20)] for j in range(20)]
    Pi = world.initPolicy(empty, initType = "biased")
    V = [[0 for i in range(20)] for j in range(20)]
    V = policyEvaluation(Pi, V) # init eval before improvement
    stable = False

    # improvement step: 
    n = 0
    while (stable == False) and n < 100:
        stable = True
        for i in range(20):
            for j in range(20):
                world.state = (i,j)
                if (i,j) == world.goal:
                    Pi[i][j] = -1
                    continue
                best = np.argmax(world.computeValues(V))
                mxm = max(world.computeValues(V))
                if best != Pi[i][j]:
                    stable = False
                    Pi[i][j] = best
        if stable == False:
            V = policyEvaluation(Pi, V)
        else:
            print("State Space Sweeps: ", n)
        n += 1
    return Pi, V


# Plots/ Heatmaps / Trajectories

def plotValueMap(optValue):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ticks = np.arange(.5, 19.5, 1)
    tick_labels = np.arange(0,19,1)
    ax.set_xticks(ticks, labels = tick_labels)
    ax.set_yticks(ticks, labels = tick_labels)
    plt.imshow(optValue, cmap ="viridis", origin = "lower")
    plt.title("Value Iteration With Goal: {0}".format(setgoal))
    plt.grid()
    plt.colorbar()
    plt.show()
    # labeling --> except overlaps look bad
    """for i in range(size):
        for j in range(size):
            text = ax.text(j, i, curr[i][j]),"""
    return

def plotPolicyMap(optPolicy):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ticks = np.arange(.5, 19.5, 1)
    tick_labels = np.arange(0,19,1)
    ax.set_xticks(ticks, labels = tick_labels)
    ax.set_yticks(ticks, labels = tick_labels)
    plt.imshow(optPolicy, cmap ="Greens", origin = "lower")  # viridis, cividis, rainbow, twilight, looks pretty good
    plt.title("Optimal Policy With Target: {0}".format(setgoal))
    
def plotSimPath(trajectory, policy):
    for state in trajectory:
        if state == goal:
            return
        else:
            i, j = state[0], state[1]
            act = policy[i][j]
            if act == 0:
                plt.arrow(j,i, 0, .4, width = .2, head_length = .3, head_starts_at_zero = True, color ='r')
            elif act == 1:
                plt.arrow(j,i, 0, -.4, width = .2, head_length = .3, head_starts_at_zero = True, color ='r')
            elif act == 2:
                plt.arrow(j,i, -.4, 0, width = .2, head_length = .3, head_starts_at_zero = True, color ='r')
            else:
                plt.arrow(j,i, .4, 0, width = .2, head_length = .3, head_starts_at_zero = True, color ='r')
    return   


def main():
    #### Value Iteration #######
    optValue = valueIteration()
    optPolicy = world.extractPolicy(optValue)
    
    #### Policy Iteration ########
    #optPolicy, optValue = policyIteration()

    #### simulate movement ####
    path, moves = world.simulateWorld(start = initial, Pi = optPolicy)

    #####  Plots ########
    plotValueMap(optValue)  # Value Function:
    fig = plt.figure()  # Policy plot
    ax = fig.add_subplot(1, 1, 1)
    ticks, tick_labels  = np.arange(.5, 19.5, 1), np.arange(0,19,1)
    ax.set_xticks(ticks, labels = tick_labels)
    ax.set_yticks(ticks, labels = tick_labels)
    plotPolicyMap(optPolicy)
    plt.grid(), plt.colorbar(), plotSimPath(path, optPolicy) 
    plt.show()
    
    return

main()



