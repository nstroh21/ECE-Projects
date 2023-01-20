import numpy as np
import matplotlib.pyplot as plt
import random

class gridworld(object):
    def __init__(self, size = 20, start = (0,0), goal = (19,9), p = 0.6, gamma = .95):
        self.size, self.goal, self.p, self.gamma = size, goal, p, gamma 
        self.start, self.state = start, start
        self.optValues = np.zeros((self.size, self.size))
        self.optPolicy = np.zeros((self.size, self.size))

    # [0,1,2,3] = [up, down, right, left]
    def move(self, action):
        if action == 0:   # up
            if self.state[0] < self.size - 1:
                self.state = (self.state[0] + 1, self.state[1])
            else:
                print("boundary, no movement")
                print(self.state)
        elif action == 1: #down
            if self.state[1] > 0:
                self.state = (self.state[0] - 1, self.state[1])
            else:
                print("boundary, no movement")
                print(self.state)
        elif action == 2: #left
            if self.state[1] > 0:
                self.state = (self.state[0], self.state[1] - 1)
            else:
                print("boundary, no movement")
                print(self.state)
        elif action == 3: #right
            if self.state[1] < self.size - 1:
                self.state = (self.state[0], self.state[1] + 1)
            else:
                print("boundary, no movement")
                print(self.state)
        else:
            pass
    
    # [0,1,2,3] = [up, down, left, right]
    def initPolicy(self, states, initType = ["random", "biased"]):
        if initType == "random":
            for i in range(self.size):
                for j in range(self.size):                
                    n = np.random.random()
                    if n <= .25:
                        action = 0
                    elif .25 < n <= .5:
                        action = 1
                    elif .5 < n <= .75:
                        action = 2
                    else:
                        action = 3
                    states[i][j] = action
        else: 
            for i in range(self.size):
                for j in range(self.size): 
                    if (j == self.goal[1]) & (i <= self.goal[0]):
                        states[i][j] = 0   # up
                    elif (j == self.goal[1]) & (i > self.goal[0]):
                        states[i][j] = 1   # down
                    elif j > self.goal[1]:
                        states[i][j] = 2  # left
                    elif j < self.goal[1]:
                        states[i][j] = 3  # right
                    else:
                        pass
        return states

    # neighbors: (up, down, right, left)
    def computeValues(self, values):
        nbrs, r = self.getNeighbors(), 0
        # base case
        if self.state == self.goal: 
            return 1
        test = [0,0,0,0]  # test each direction
        for move in [0, 1, 2, 3]:   # [up, down, "right", "left" ]    
            if nbrs[move] == None:
                continue
            else:
                for s in nbrs:
                    if s == None:  #boundary
                        continue
                    if nbrs.index(s) == move:  # use correct transition factor
                        T = self.p
                    else:
                        T = (1-self.p)/3
                    test[move] += T*(r+self.gamma*values[s[0]][s[1]])  # bellman's equation, r is always 0 here
        # having trouble with direct update, np array will not set to a variable
        # self.currValues[self.state] = max(test)
        return test

    # generate a policy given only an optimal value function/somewhat redundant
    def extractPolicy(self, V = [[]]):
        policy = [[ 0 for i in range(20)] for j in range(20)]
        for i in range(self.size):
            for j in range(self.size):
                self.state = (i,j)
                if self.state == self.goal:
                    policy[i][j] = -1
                    continue
                else:
                    nbrs = self.getNeighbors()
                    values = []
                    for n in nbrs:
                        if n != None:
                            q, r = n[0], n[1]
                            values.append(V[q][r])
                        else:
                            values.append(-1)
                    policy[i][j] = np.argmax(values)
        return policy

    def computePolicyStep(self, move = 0, values = [[]], nbrs = []):
        test = 0
        if self.state == self.goal: 
            return 10   # for some reason I needed to hardcode in a much higher reward here to converge properly
        for s in nbrs:
            if s == None:
                continue
            if s == self.goal:
                r = 1
            else:
                r = 0
            if nbrs.index(s) == move:
                T = self.p
            else:
                T = (1-self.p)/3          
            test += T*(r+self.gamma*values[s[0]][s[1]])
        return test
    
    def checkStop(self, prev, curr):
        diff = 0
        for i in range(self.size):
            for j in range(self.size):
                diff += abs((prev[i][j] - curr[i][j]))
        return diff
    
    def getNeighbors(self):  # check bounds and get neighbors if exists, "up" actually decreases row num
        if self.state[0] < self.size-1:
            up = (self.state[0] + 1, self.state[1])
        else:
            up = None
        if self.state[0] > 0:
            down = (self.state[0] - 1, self.state[1])
        else:
            down = None
        if self.state[1] < self.size-1:
            right = (self.state[0], self.state[1] + 1)
        else:
            right = None
        if self.state[1] > 0:
            left = (self.state[0], self.state[1] - 1)
        else:
            left = None

        return [up, down, left, right]
    
    # based on a computed optiaml policy pi and initial state, simulate the MDP
    def simulateWorld(self,start = (0,0), Pi = [[]]):
        self.state = start
        states, actions = [start], []
        i, j = start[0], start[1]
        go, iter = True, 0
        while (go == True) & (iter < 1000):
            action = Pi[i][j]
            actions.append(action)
            self.move(action)
            new = self.state
            if new == self.goal:
                print("Target State Achieved")
                go = False
            states.append(new)
            i, j = new[0], new[1]
            iter += 1
        return states, actions
        
    
    



        

