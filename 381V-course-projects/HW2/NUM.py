import cvxpy as cp
import numpy as np
from matplotlib import pyplot as plt

# network utilit maximization , # for loop for capacity sensitivity analysis
sols1 = []
sols2 = []
for i in (0,-1):
    cap1 = 10+i
    sols = []

    a = np.array([1, 4, 2, 3, 5])
    B = np.array([2, 1, 5, 3, 4])
    x = cp.Variable(len(a))
    constraints = [x >= 0 , cp.sum(x) == cap1]
    objective = cp.Minimize(-cp.sum(cp.multiply(a, cp.log(B + x))))

    problem1 = cp.Problem(objective, constraints)
    problem1.solve()
    sols1.append(problem1.value)

    # capacity sensitivity analysis
    cap2 = 100+i
    constraints2 = [x >= 0 , cp.sum(x) == cap2]
    problem2 = cp.Problem(objective, constraints2)
    problem2.solve()
    sols2.append(problem2.value)

# print(sols1[0], "\n", sols1[1], "\n", abs(sols1[0] - sols1[1]))
print("Capacity = 10 Sensitivity:", abs(sols1[0] - sols1[1]), "Capacity = 100 Sensitivity:", abs(sols2[1] - sols2[0]))
#print(sols1, "\n", sols2)

# calculating marginal utilities
#uprime0 = a/B
#uprime = a/(B+values)
#print(constraints[1].dual_value)

#print("Marginal utilities are:" , uprime)
#print("Optimal allocation is:", values)
#print("Overall network allocation is", np.sum(values))


#Plots
"""
threshold = 1/lambda_star
y = np.array([0,1, 2, 3, 4])
fig, ax = plt.subplots()
ax.bar(y, B, color = "skyblue")
#ax.plot([-1,5], [threshold, threshold], "--", color = "r",  linewidth=2.2)
#plt.text(-.9, threshold + (.03*threshold),'1/\u03BB*', size = 'large' )
plt.xlim([-1,5])
plt.ylim([0,10])
plt.xlabel("Channels")
plt.ylabel("Rate Allocations") 
plt.title("Network Rates (Before)")
plt.show()


y = np.array([0,1, 2, 3, 4])
fig, ax = plt.subplots()
ax.bar(y, uprime0, color = "salmon")
#ax.plot([-1,5], [threshold, threshold], "--", color = "r",  linewidth=2.2)
#plt.text(-.9, threshold + (.03*threshold),'1/\u03BB*', size = 'large' )
plt.xlim([-1,5])
plt.ylim([0,5])
plt.xlabel("Channel")
plt.ylabel("Marginal Utility") 
plt.title("Intial Marginal Utilities")
plt.show()

B = x.value + B

fig, ax = plt.subplots()
ax.bar(y, a, color = "skyblue")
#ax.plot([-1,5], [threshold, threshold], "--", color = "r",  linewidth=2.2)
#plt.text(-.9, threshold + (.03*threshold),'1/\u03BB*', size = 'large' )
plt.xlim([-1,5])
plt.ylim([0,10])
plt.xlabel("Channels")
plt.ylabel("Rate Allocations") 
plt.title("Network rates (After)")
plt.show()

y = np.array([0,1, 2, 3, 4])
fig, ax = plt.subplots()
ax.bar(y, uprime, color = "salmon")
#ax.plot([-1,5], [threshold, threshold], "--", color = "r",  linewidth=2.2)
#plt.text(-.9, threshold + (.03*threshold),'1/\u03BB*', size = 'large' )
plt.xlim([-1,5])
plt.ylim([0,5])
plt.xlabel("Channel")
plt.ylabel("Marginal Utility") 
plt.title("Final Marginal Utilities")
plt.show() """

