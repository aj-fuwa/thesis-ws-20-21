'''
# Name: curve_fitting_for_dist.py
# Aim: To do curve fitting for our distance measurement
# Date: (Revised) 1.Feb 2021
# Src:  https://www.youtube.com/watch?v=Dggl0fJJ81k
'''
import numpy as np

y = [0, 30]     # these are the cm values. RHS and LHS values
x = [500, 40]   # these are the coordinates on the screen. RHS and LHS values
                # (0,0) is on the left top corner of the screen. Y increases downwards, X increases on the right

curve = np.polyfit(x, y, 2)     # fit the data with eqn of 2nd order
poly = np.poly1d(curve)         # get the equation

print(poly)         # print the equation
print(poly(320))    # predict the value of Y for a given X





