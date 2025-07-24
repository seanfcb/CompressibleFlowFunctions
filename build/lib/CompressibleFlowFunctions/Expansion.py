import numpy as np
import sys
from scipy.optimize import *

def prandtl_meyer(M, gamma):
    '''
    Function calculates the Prandtl-Meyer expansion angle nu knowing the flow Mach number M and ratio of specific heats gamma.
    Expected inputs:
    M        : Mach number
    gamma    : Ratio of specific heats
    '''
    term1 = np.sqrt((gamma + 1) / (gamma - 1))
    term2 = np.arctan(np.sqrt((gamma - 1) * (M**2 - 1) / (gamma + 1)))
    term3 = np.arctan(np.sqrt(M**2 - 1))
    nu = term1 * term2 - term3
    return nu

def mach_angle(M):
    '''
    Function calculates the Mach angle mu knowing the Mach number.
    Expected inputs:
    M       : Mach number
    '''
    mu = np.arcsin(1/M)
    return mu