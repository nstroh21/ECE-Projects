# Class Link: https://utexas.instructure.com/courses/1342654/files/folder/Lecture%20Notes/Lectures%204%20and%205%20-%20Tracking%20iLQR?
# Helpful Github : https://github.com/studywolf/control/blob/master/studywolf_control/controllers/ilqr.py


# user defined nonlinear function -- "apply_dynamics"

# given non-zero reference trajectory {xo, x1, x2, x3 ...}
# So we are starting with x_N, or maybe x_o is the final goal?
# given non-zero control policy: (uo, u1, u2, ....)



# LQR COST :  decision variables are dx and dq (deltas)
# dx = (xk - xbar_k)
# du = (uk - ubar_k)

# sum: dxQdx _ duRdu + qdx + rdu + dxHdu
# subject to: x_k+1 = Akdxk  + Bk duk  # A, B are jacobians b


# if we have x (current state), linearize dynamics locally
# Template: f_lin = f(xk) + gradientf(xk)*(x).transpose()*(x-xk) + (x-xk).transpose()*(Hessian(xk))*(x-xo)
# if we have a vector function then these need to become jacobians not just gradients

# Next Step is to quadratize the cost function as well
# Q, R, q, r, H -- H is for the cross term

# Use these matrices and the LQR package provided in class -- although it may need to be modified to use q,r,H

# Backward Prop
# LQR will return K matrix, which has optimal weights for duk (stage policy -- delta)
# u_optimal = u + duk (add to our policy vector)

# Forward Prop
# get the new state from u_optimal and xk , use the orginal non-linear dynamics :
# x_k+1 = f(x_k, u_optimal)

# iterate until we get all N policies in u vector

