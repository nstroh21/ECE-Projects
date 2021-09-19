#state machine class will go here:

class SM:
    # default attributes and methods:
    startState = None
    # by default the output is also just the next state of the machine
    def getNextValues(self, state, inp):
        nextState = self.getNextState(state, inp)
        return (nextState, nextState)
    # running the machine
    def start(self):
        self.state = self.startState
    # a single step represents the transition of states and generates an ouput from an input & prior state
    def step(self, inp, verbose = False):
        (s,o) = self.getNextValues(self.state, inp)
        self.state = s
        if (verbose == False):
            return o
        else:
            return (o, s)
    # transduce produces a string of outputs from a string of inputs -- representing "continuous" time
    def transduce(self, inputs, verbose = False):
        self.start() # this line starts the machine by setting the state to the start state
        if (verbose == False):
            return [self.step(inp) for inp in inputs] #list comprehension which assumes the inputs are passed as a list
        else:
            return [self.step(inp, verbose == True) for inp in inputs]


    