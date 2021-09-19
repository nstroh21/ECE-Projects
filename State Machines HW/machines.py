# This file to house different practice problems building state machine of the parent class SM

from SM import SM

# some common machines discussed in class:

class Delay(SM):
    def __init__(self, v0):
        self.endState = v0
    def getNextValues(self, state, inp):
        return (inp, state)


### More ... 


#this first machine will intake a string and will output characters if they are a part of a comment or None if not
# we do want the # to be printed too -- we want to call the inputs in such a way to fast forward by 1
# we don't need a constructor because we don't have to pass any attributes to the machine
class commentsSM(SM):
    startState = "Not"
    def getNextState(self, state, inp):
        if (state == "Not") and (inp == '#'):
            nextState = "Comment"
        elif (state == "Comment") and (inp == '\n'):
            nextState = "Not"
        else: 
            nextState = state
        return nextState
    
    def generateOutputs(self, state, inp):
        nextState = self.getNextState(state, inp)
        if (nextState == "Comment"):
            output = inp
        else:
            output = None
        return output

    def getNextValues(self, state, inp):
        s = self.getNextState(state, inp)
        o = self.generateOutputs(state, inp)
        return (s,o)

# this machine takes in a string and determines which "words" are the first word on the line
# the states should be "Not" or "First"
# the machine will begin in "First" and transition to "First" when "/n" is the input
# the machine will transition back to not when " " is the input
# actually going to create a 3rd state called "newline" when we get a new line but it begins with white space
class firstWordSM(SM): 
    startState = "First"
    def getNextState(self, state, inp):
        if (state == "First") and (inp == ' '):
            nextState = "Not"
        elif (inp == '\n'):
            nextState = "newline"
        elif (state == 'newline') and (inp != ' '):
            nextState = "First"
        else: 
            nextState = state
        return nextState
    
    def generateOutputs(self, state, inp):
        nextState = self.getNextState(state, inp)
        if (state == "First") and (nextState == "First"):
            output = inp
        elif (state == 'newline') and (nextState == 'First'):
            output = inp
        else:
            output = None
        return output

    def getNextValues(self, state, inp):
        s = self.getNextState(state, inp)
        o = self.generateOutputs(state, inp)
        return (s,o)

# The next machine is the Counting State Machine
# It inherits from SM but other state machines will also inherit from it
# it will be used to keep count of every step in a trnasduce call --- in other words it increments 

class  countingSM(SM): 
    startState = 0
    state = startState
    def getNextState(self, state, inp):
        return state + 1
    def generateOutputs(self, state, inp):
        out = self.getOutput(state, inp) # so do I or do I not need keyword super() ? 
        # Notice however I do need to remove "self" from attributes here -- i think what that means is it looks in the same class for the method? 
        return out
    def getOutput(self, state, inp):
        return 1
    def getNextValues(self, state, inp):
        s = self.getNextState(state, inp)
        o = self.generateOutputs(state, inp)
        return (s,o)

## Counting sub-machines that inherit from the counting machine
#example machine given in class
class CountMod5(countingSM):
    startState = 50
    def getOutput(self, state, inp):
        #return super(CountMod5, self).getOutput(state,inp)  #this actually calls the parent method By default the child method is considered first in MRO 
        return state % 5
#exercise question -- a superclass can "know" attributes of the subclass        
class alternateZeroes(countingSM):
    state  = countingSM.state
    def getOutput(self, state, inp):
        out = 0
        if (state % 2 == 0):
            out = inp
        else:
            out = 0
        return out



### Also To DO:  read about cascading state machines and then create the "cascade" machine which will take 2 state
###               machines as its input and then generate cascaded outputs

##Combinator Machines:

class Cascade(SM):
    startState = (0,0)
    def __init__(self, sm1, sm2):
        # first state of the machine which actually be 2nd machines state -- which is output first
        self.sm1 = sm1
        self.sm2 = sm2
        self.startState = (self.sm1.startState, self.sm2.startState)

    def getNextValues(self, state, inp):
        sm1_nextState,sm1_out = self.sm1.getNextValues(state[0], inp)
        sm2_nextState, sm2_out = self.sm2.getNextValues(state[1], sm1_out)

        return ((sm1_nextState, sm2_nextState), sm2_out)


