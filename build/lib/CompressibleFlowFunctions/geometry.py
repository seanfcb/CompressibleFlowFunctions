import numpy as np
import sys


def frustum(ri, ro, s):
    '''
    Function calculates the surface area of a truncated cone, otherwise known as a frustum, knowing the major and minor radii, and the length of the surface between those radii
    Expected inputs:

    ri        : minor radius
    ro        : major radius
    s         : cone surface length

    Returns: Surface area of the truncated cone
    '''
    A = np.pi(ro**2+ri**+s*(ro+ri))
    return A