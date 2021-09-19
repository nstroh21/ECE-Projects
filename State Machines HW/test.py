import machines

# test the comments machine with th below variable string
comTestStr = '''# does this
#one
#work
or no
#yes'''
CM = machines.commentsSM()
#print(CM.transduce(comTestStr, verbose = False))
firstTestStr = '''does
this
1
work
      ##
def f(x): # comment
return 1''' 
#FirstSM = machines.firstWordSM()
#print(FirstSM.transduce(firstTestStr))

# countingMachine inheritance test
"""mod5M = machines.CountMod5()
print(mod5M.transduce([0,1,2,3,4,5,6,7,8,9,10]))

alternate = machines.alternateZeroes()
print(alternate.transduce([1,2,3,4,5,6,7,8,9,10]))"""


# testing the cascade combinator with 2 dealy machines

d1 = machines.Delay(99)
d2 = machines.Delay(22)
cas = machines.Cascade(d1, d2)

print(cas.transduce([3, 8, 2, 4, 6, 5]))

