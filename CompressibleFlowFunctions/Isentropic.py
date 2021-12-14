import numpy as np
import sys
from scipy.optimize import *


def astar_all_else_known(Dpipe,M,gamma):
    '''
    Function calculates the choking area (and diameter) using the compressible area ratio knowing all other properties
    Expected inputs:
    Dpipe    : Diameter of pipe, meters
    M        : Mach number
    gamma    : Ratio of specific heats

    '''
    Apipe  = np.pi*Dpipe**2/4
    Aratio = aratio_from_mach(M,gamma)
    Astar  = Apipe/Aratio
    Dstar  = np.sqrt(Astar*4/np.pi)
    return Astar, Dstar

def mach_from_G(Po,Rs,To,gamma,mdot,Dpipe,subsuper):
    '''
    Calculates the Mach number knowing all other flow properties. This function allows the user to specify whether to resolve to the subsonic or supersonic branch
    Expected inputs:
    Po       : Stagnation pressure, Pa
    Rs       : Specific gas constant, J/kgK (double check units)
    To       : Stagnation temperature, K
    gamma    : Ratio of specific heats
    mdot     : Mass flow rate, kg/s
    Dpipe    : Diameter of pipe, meters
    subsuper : Specify either 'subsonic' or 'supersonic'
    '''
    Apipe = np.pi*Dpipe*Dpipe/4
    def delta_G(M,Po,Rs,To,gamma,mdot,Apipe):
        return mdot/Apipe - Po*np.sqrt(gamma/Rs/To)*M*(1+(gamma-2)/2*M*M)**(-(gamma+1)/(2*(gamma-1)))
    if subsuper == 'subsonic':
        M = bisect(delta_G,0.00001,0.99,args=(Po,Rs,To,gamma,mdot,Apipe))
    elif subsuper == 'supersonic':
        M = bisect(delta_G,1,99,args=(Po,Rs,To,gamma,mdot,Apipe))
    else:
        sys.exit('Please specify whether you want to resolve to the "subsonic" or "supersonic" branch when calling mach_from_G')

    return M

def mach_from_aratio(Apipe,Astar,gamma,subsuper):
    '''
    Function calculates the Mach number at a given location using the compressible area ratio knowing all other properties
    Expected inputs:
    Apipe    : Pipe area, sq. m
    Astar    : Choking area, sq. m
    gamma    : Ratio of specific heats
    subsuper : Specify either 'subsonic' or 'supersonic'
    '''
    def arat_delta(M,gamma,Apipe,Astar):
        return Apipe/Astar - aratio_from_mach(M,gamma)
    if subsuper == 'subsonic':
        M = bisect(arat_delta,0.00001,0.99,args=(gamma,Apipe,Astar))
    elif subsuper == 'supersonic':
        M = bisect(arat_delta,1,99,args=(gamma,Apipe,Astar))
    else:
        sys.exit('Please specify whether you want to resolve to the "subsonic" or "supersonic" branch when calling mach_from_aratio')
    return M

def mach_from_massflow(Apipe,mdot,Po,To,Rs,gamma,subsuper):
    '''
    Function calculates the Mach number at a given location using the compressible area ratio knowing all other properties
    Expected inputs:
    Apipe    : Pipe area, sq. m
    mdot     : Mass flow rate, kg/s
    Po       : Stagnation pressure, Pa
    To       : Stagnation temperature, K
    Rs       : Specific gas constant, J/kgK (double check units)
    gamma    : Ratio of specific heats
    subsuper : Specify either 'subsonic' or 'supersonic'
    '''
    Dpipe   = np.sqrt(4*Apipe/np.pi)
    def g_delta(M,Po,To,Rs,gamma,Dpipe,Apipe,mdot):
        return mdot/Apipe - mass_from_area(M,Po,To,Rs,gamma,Dpipe)
    if subsuper == 'subsonic':
        M = bisect(g_delta,0.00001,0.99,args=(Po,To,Rs,gamma,Dpipe,Apipe,mdot))
    elif subsuper == 'supersonic':
        M = bisect(g_delta,1,99,args=(Po,To,Rs,gamma,Dpipe,Apipe,mdot))
    else:
        sys.exit('Please specify whether you want to resolve to the "subsonic" or "supersonic" branch when calling mach_from_massflow')

    return M

def aratio_from_mach(M,gamma):
    '''
    Function calculates the compressible area ratio A/Astar knowing the Mach number and gamma
    Expected inputs:
    M        : Mach number
    gamma    : Ratio of specific heats
    '''
    Aratio = ((gamma+1)/2)**(-(gamma+1)/(2*(gamma-1)))*(1+(gamma-1)/2*M*M)**((gamma+1)/(2*(gamma-1)))/M
    return Aratio

def po_from_pratio(P,gamma,M):
    '''
    Function calculates the static pressure knowing the gas properties, Mach number, and stagnation pressure using the isentropic pressure ratio equation P/Po
    Expected inputs:
    Po       : Stagnation pressure, any units can be used. Static pressure will be returned in the same units provided for stagnation pressure
    gamma    : Ratio of specific heats
    M        : Mach number
    '''
    Po = P/(1+((gamma-1)/2)*M**2)**(-(gamma)/(gamma-1))
    return Po

def p_from_pratio(Po,gamma,M):
    '''
    Function calculates the static pressure knowing the gas properties, Mach number, and stagnation pressure using the isentropic pressure ratio equation P/Po
    Expected inputs:
    Po       : Stagnation pressure, any units can be used. Static pressure will be returned in the same units provided for stagnation pressure
    gamma    : Ratio of specific heats
    M        : Mach number
    '''
    P_static = Po*(1+((gamma-1)/2)*M**2)**(-(gamma)/(gamma-1))
    return P_static

def T_from_Tratio(To,gamma,M):
    '''
    Function calculates the static pressure knowing the gas properties, Mach number, and stagnation pressure using the isentropic pressure ratio equation P/Po
    Expected inputs:
    To       : Stagnation temperature, K
    gamma    : Ratio of specific heats
    M        : Mach number

    '''
    return To/(1+((gamma-1)/2)*M**2)

def To_from_Tratio(To,gamma,M):
    '''
    Function calculates the static pressure knowing the gas properties, Mach number, and stagnation pressure using the isentropic pressure ratio equation P/Po
    Expected inputs:
    T       : Stagnation temperature, K
    gamma    : Ratio of specific heats
    M        : Mach number

    '''
    return T*(1+((gamma-1)/2)*M**2)

def mach_from_Tratio(M,To,T1,gamma):
    return T_from_Tratio(To,gamma,M)-T1

def delta_mass_static(M,mdot,P,Rs,To,gamma,A):
    '''
    Using the mdot over astar equation for choked flow combined with the P/Po equation, provides an equation to iterate on knowing all other parameters.
    Expected inputs:
    M        : Mach number of the flow
    mdot     : Mass flow rate, g/s
    P        : Static pressure, Pa
    Rs       : Specific gas constant, J/kgK (double check units)
    To       : Stagnation temperature, K
    gamma    : Ratio of specific heats
    A        : Cross-sectional area of the pipe in sq. m
    '''

    return mdot/1000 - P*(1+(gamma-1)/2*M*M)**(gamma/(gamma-1))*A*np.sqrt(gamma/(Rs*To))*M*(1+(gamma-1)/2*M*M)**(-(gamma+1)/(2*(gamma-1)))

def delta_mass_stag(M,mdot,Po,Rs,To,gamma,A):
    '''
    Using the mdot over astar equation for choked flow, provides an equation to iterate on knowing all other parameters.
    Expected inputs:
    M        : Mach number of the flow
    mdot     : Mass flow rate, g/s
    Po       : Stagnation pressure, Pa
    Rs       : Specific gas constant, J/kgK (double check units)
    To       : Stagnation temperature, K
    gamma    : Ratio of specific heats
    A        : Cross-sectional area of the pipe in sq. m
    '''
    return mdot/1000 - A*Po*np.sqrt(gamma/(Rs*To))*M*(1+(gamma-1)/2*M*M)**((-(gamma+1))/(2*(gamma-1)))

##==================================================================##
## Functions removed from library
##==================================================================##


# def area_from_mass(Po,To,Rs,gamma,mdot):
#     '''
#     Function calculates the choking area using the compressible area ratio
#     Expected inputs:
#     Po       : Stagnation pressure, Pa
#     To       : Stagnation temperature, K
#     Rs       : Specific gas constant, J/kgK (double check units)
#     gamma    : Ratio of specific heats
#     mdot     : Mass flow rate, kg/s
#     '''
#     Astar = mdot/(Po*np.sqrt(gamma/(Rs*To))*((gamma+1)/2)**(-(gamma+1)/(2*(gamma-1))))##We call Gstar the ratio mdot/Astar
#     return Astar
#
# def mass_from_area(M,Po,To,Rs,gamma,Area):
#     '''
#     Function calculates the mass flow rate using the compressible area ratio
#     Expected inputs:
#     M        : Mach number
#     Po       : Stagnation pressure, Pa
#     To       : Stagnation temperature, K
#     Rs       : Specific gas constant, J/kgK (double check units)
#     gamma    : Ratio of specific heats
#     Area     : Pipe area, sq. m
#     '''
#     #Astar = np.pi*Dpipe*Dpipe/4
#     #Gstar = Po*np.sqrt(gamma/Rs/To)*((gamma+1)/2)**(-(gamma+1)/(2*(gamma-1)))##We call Gstar the ratio mdot/Astar
#     Gstar = Po*np.sqrt(gamma/Rs/To)*M*(1+(gamma-2)/2*M*M)**(-(gamma+1)/(2*(gamma-1)))##We call Gstar the ratio mdot/Astar
#     mdot  = Gstar*Area
#     return mdot
