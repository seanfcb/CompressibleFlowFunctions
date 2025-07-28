import numpy as np
import sys
from scipy.optimize import *

def prat_from_mach(gamma,M):
    '''
    For a known pre-shock mach number, what is the stagnation pressure ratio
    Expected inputs:
    M        : Mach number
    gamma    : Ratio of specific heats
    '''
    pratio = (((gamma+1)*M*M)/((gamma-1)*M*M+2))**(gamma/(gamma-1))*((gamma+1)/(2*gamma*M*M-(gamma-1)))**(1/(gamma-1))
    return pratio

def mach_from_pressure_ratio(Po1,Po2,gamma):
    '''
    For a desired stagnation pressure ratio, this function calculates the Mach number before a NSW
        Expected inputs:
        Po1      : Stagnation pressure before a normal shock wave, units same as Po2
        Po2      : Stagnation pressure after a normal shock wave, units same as Po1
        gamma    : Ratio of specific heats
    '''
    Por  = Po2/Po1 ##Desired pressure ratio
    def Prat(Mi,gamma,Por):
        return (((gamma+1)*Mi*Mi)/((gamma-1)*Mi*Mi+2))**(gamma/(gamma-1))*((gamma+1)/(2*gamma*Mi*Mi-(gamma-1)))**(1/(gamma-1)) - Por
    M = bisect(Prat,1,100,args=(gamma,Por))
    return M

def mach_after_shock(M1,gamma):
    '''
    Calculates the Mach number after a NSW knowing the pre-shock Mach number
    Expected inputs:
    M1       : Mach number
    gamma    : Ratio of specific heats
    '''
    M2 = np.sqrt(((gamma-1)*M1*M1+2)/(2*gamma*M1*M1-(gamma-1)))
    return M2

def pstatic_after_shock(M,gamma,P):
    '''
    Calculates the static pressure after a NSW knowing the pre-choke Mach number, gamma, and static pressure
    Expected inputs:
    M        : Mach number
    gamma    : Ratio of specific heats
    P        : Static pressure before a normal shock wave
    '''
    P2 = P*(2*gamma*M*M-(gamma-1))/(gamma+1)
    return P2

def pstag_after_shock(M,gamma,Po1):
    '''
    Calculates the stagnation pressure after a NSW knowing the pre-choke Mach number, gamma
    Expected inputs:
    M        : Mach number
    gamma    : Ratio of specific heats
    Po1      : Stagnation pressure before a normal shock wave
    '''
    Po2 = Po1*(((gamma+1)*M*M)/((gamma-1)*M*M+2))**(gamma/(gamma-1))*((gamma+1)/(2*gamma*M*M-(gamma-1)))**(1/(gamma-1)) ##Solution from the NSW stagnation pressure ratio equation.
    return Po2
