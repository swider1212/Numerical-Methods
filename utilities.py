

# return [epsilon/n, x]

import re
import numpy as np
from scipy.misc import derivative
import math as mt

def horner_algoritm(n,x,poly):
    result = poly[0]
    for i in range(1, n):
        result = result*x + poly[i]
    return result    
    
def first (x, diff = False):
    if diff:
        return 3*x**2-2*x-2

    poly_first=[1,-1,-2,1]
    n_first=len(poly_first)
    return horner_algoritm(n_first,x,poly_first)

def fourth (x, diff = False):
    if diff:
        return 3*x**2 - 1
    poly_fourth=[1,0,-1,1]
    n_fourth=len(poly_fourth)
    return horner_algoritm(n_fourth,x,poly_fourth)

def second (x, diff = False):
    if diff:
        return (2**x)*mt.log(2)-3
    return 2**x-3*x

def third (x, diff = False):
    if diff:
        e=np.exp(1)
        return -e**x + np.cos(x) + 3        
    e=np.exp(1)
    return 3*x+np.sin(x)-e**x

def fifth (x, diff = False):
    if diff:
        return (1/np.cos(x))**2
    return np.tan(x)-1

def sixth (x, diff = False):
    if diff:
        return -2*np.sin(2*x)
    return 2 + np.cos(2*x)

def seventh (x, diff = False):
    if diff:
        return np.sin(x) + np.cos(x)
    return np.sin(x) - np.cos(x)


all_functions = [first, second, third, fourth, fifth, sixth, seventh]

def half_algoritm(board_function,left,right,metodh,iteration_epsilon):
    if board_function(left)*board_function(right) > 0:
        return False
    else:
        if metodh == 1:
            n = 0
            x = 0
            while n < iteration_epsilon:
                if(board_function(x) == 0.0):
                    return [n, x, board_function(x)]
                x = (left + right)/2
                # print(left, ":", right,"| x:",  x, "f(x): ", board_function(x))
                if board_function(x)*board_function(right) < 0:
                    left = x
                else:
                    right = x
                n+=1
            return [n, x]
        elif metodh == 2:
            n = 0
            x1 = x2 = (left + right)/2
            while 1:
                if board_function(x1)*board_function(right) < 0:
                    left = x1
                else :
                    right = x1
                x2 = x1
                x1 = (left + right)/2
                n+=1
                if(iteration_epsilon > np.absolute(x1-x2)):
                    return [n, x1]
            return [n, x1]
    
def newton_algoritm(board_function,left,right,metodh,iteration_epsilon):
    n = 0
    x1 = right
    x2 = 0
    if board_function(left)*board_function(right) > 0:
        return False
    else:
        if metodh == 1:
            while n < iteration_epsilon:
                x2 = x1 - board_function(x1)/board_function(x1, True)
                x1 = x2
                n += 1
            return [n, x2]
        elif metodh == 2:
            n = 0
            while 1:
                x1 = x2
                x2 = x1 - board_function(x1)/board_function(x1, True)
                if(iteration_epsilon > np.absolute(x1-x2)):
                    return [n, x2]
                n += 1
            return [n, x2]


# half_algoritm(fifth)
# half_algoritm(eight,-10,10,2,.0001)
# newton_algoritm(first,-10,10,1,10,first_diff)