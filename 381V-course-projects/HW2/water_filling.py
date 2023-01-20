import cvxpy as cp
import numpy as np
from matplotlib import pyplot as plt
#import math

# problem data: water filling for the initial allocation given below
# a = np.array([1.2, 0.9, 1.3, 0.7, 0.8])
a = np.array([.5, 0.5, 0.5, 0.5, 0.5])
x = cp.Variable(len(a))
constraints = [x >= 0 , cp.sum(x) <= 1]
objective = cp.Minimize(-cp.sum(cp.log(a + x)))

# solve convex minimization
prob = cp.Problem(objective, constraints)
prob.solve()
lambda_star = constraints[1].dual_value

print("The maximum utility is:", -prob.value)
print("The optimal x_i's are", x.value )
print("The optimal allocation is", x.value + a)
print("The lagrange mult for the first constraint:", constraints[0].dual_value)
print("The lagrange mult for the second constraint:", constraints[1].dual_value)
print("The single channel water level max is" , 1/(constraints[1].dual_value))


# check, calculate the objective with a slight deviation:
# optimal
"""
a = np.array([1.20000002, 1.13333332, 1.30000001, 1.33333333, 1.13333332])
print("Optimal Utility:", cp.sum(cp.log(a)).value)
# test various deviations:
a[0] = a[0] - .0001
a[1] = a[1] + 0           # .0001, seems to have made it sub-opt?
a[2] = a[2] + 0
a[3] = a[3] + 0.0001
a[4] = a[4] + 0
print("Deviated Utility:", cp.sum(cp.log(a)).value)
""" 
# Need to create a plot

threshold = 1/lambda_star
y = np.array([0,1, 2, 3, 4])
fig, ax = plt.subplots()
ax.bar(y, a, color = "skyblue")
ax.plot([-1,5], [threshold, threshold], "k--", color = "r",  linewidth=2.2)
plt.text(-.9, threshold + (.03*threshold),'1/\u03BB*', size = 'large' )
plt.xlim([-1,5])
plt.ylim([0,2])
plt.xlabel("Channels")
plt.ylabel("Water Level") 
plt.title("Water Filling (Before)")
plt.show()

a = x.value + a

fig, ax = plt.subplots()
ax.bar(y, a, color = "skyblue")
ax.plot([-1,5], [threshold, threshold], "k--", color = "r",  linewidth=2.2)
plt.text(-.9, threshold + (.03*threshold),'1/\u03BB*', size = 'large' )
plt.xlim([-1,5])
plt.ylim([0,2])
plt.xlabel("Channels")
plt.ylabel("Water Level") 
plt.title("Water Filling (After)")
plt.show()