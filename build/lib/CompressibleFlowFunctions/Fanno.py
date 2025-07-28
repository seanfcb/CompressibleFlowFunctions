import numpy as np
import sys
from scipy.optimize import *


def colebrook_white(f,Re,D,epsilon):
    '''
    Subtracts both sides of the Colebrook-White equation to calculate the Darcy friction factor.
    Divide the result by 4 for the Fanning friction factor.
    Expected inputs:
    f       : Darcy friction factor
    Re      : Reynolds Number
    D       : Pipe diameter
    epsilon : Surface roughness in micrometers
    '''
    return 1/np.sqrt(f) - (-2)*np.log10(epsilon/(3.7*D) + 2.51/(Re*np.sqrt(f)))

def fanno_equation(M,gamma):
    return ((1-M**2)/(gamma*M**2) + (gamma+1)/(2*gamma)*np.log(((gamma+1)*M**2)/(2*(1+(gamma-1)/2*M**2))))

def delta_fanno(M,L,f,D,gamma):
    '''
    Function returns the sum of the left hand side and right hand side of the Fanno equation.
    Expected inputs:
    M       : Inlet Mach number
    L       : Choking pipe length
    f       : Fanning friction factor
    D       : Pipe diameter
    gamma   : Ratio of specific heats
    '''
    return ((1-M**2)/(gamma*M**2) + (gamma+1)/(2*gamma)*np.log(((gamma+1)*M**2)/(2*(1+(gamma-1)/2*M**2))))-4*f*L/D

def Lstar_fanno(f,D,M,gamma): #Define the Fanno equation to iterate on
    '''
    Function directly calculates Lstar in the Fanno equation.
    Expected inputs:
    f       : Fanning friction factor
    D       : Pipe diameter
    M       : Inlet Mach number
    gamma   : Ratio of specific heats
    '''

    return ((1-M**2)/(gamma*M**2) + (gamma+1)/(2*gamma)*np.log(((gamma+1)*M**2)/(2*(1+(gamma-1)/2*M**2))))*D/(4*f)

def mach_fanno(L,f,D,gamma): #Define the Fanno equation to iterate on
    '''
    Wraps the delta_fanno function to calculate a Mach number
    Expected inputs:
    L       : Choking pipe length
    f       : Fanning friction factor
    D       : Pipe diameter
    gamma   : Ratio of specific heats
    '''
    M = bisect(delta_fanno,0.001,0.99,args=(L,f,D,gamma))
    return M

def fanno_po_ratio(M,gamma):
    return (1/M)*((2+(gamma-1)*M**2)/(gamma+1))**((gamma+1)/(2*(gamma-1)))
