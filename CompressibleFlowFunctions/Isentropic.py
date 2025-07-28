import numpy as np
import sys
from scipy.optimize import *

def mdot_from_throat_area(A_throat, Po, Rs, To, gamma):
    '''
    Solves for mass flow rate (mdot) given choked area and stagnation properties.
    Expected inputs:
    A_throat : Choked area, m²
    Po       : Stagnation pressure, Pa
    Rs       : Specific gas constant, J/kgK
    To       : Stagnation temperature, K
    gamma    : Ratio of specific heats

    Returns: mdot
    '''
    term1 = A_throat * Po
    term2 = np.sqrt(gamma / (Rs * To))
    term3 = (2 / (gamma + 1)) ** ((gamma + 1) / (2 * (gamma - 1)))
    mdot = term1 * term2 * term3
    return mdot

def throat_area_from_mdot(mdot, Po, Rs, To, gamma):
    '''
    Using the mdot over astar equation for choked flow, calculate choke area knowing all other properties.
    Expected inputs:
    mdot     : Mass flow rate, kg/s
    Po       : Stagnation pressure, Pa
    Rs       : Specific gas constant, J/kgK
    To       : Stagnation temperature, K
    gamma    : Ratio of specific heats

    Returns: A_throat
    '''
    term1 = mdot / Po
    term2 = np.sqrt(Rs * To / gamma)
    term3 = (2 / (gamma + 1)) ** (-(gamma + 1) / (2 * (gamma - 1)))
    A_throat = term1 * term2 * term3
    return A_throat

def astar_all_else_known(Apipe,M,gamma):
    '''
    Function calculates the choking area (and diameter) using the compressible area ratio knowing all other properties
    Expected inputs:
    Apipe    : Pipe cross sectional area, sq. m
    M        : Mach number
    gamma    : Ratio of specific heats

    Returns: Astar, Dstar

    '''
    Aratio = aratio_from_mach(M,gamma)
    Astar  = Apipe/Aratio
    Dstar  = np.sqrt(Astar*4/np.pi)
    return Astar, Dstar



def mach_from_G(Po,Rs,To,gamma,mdot,Apipe,subsuper):
    '''
    Calculates the Mach number knowing all other flow properties. This function allows the user to specify whether to resolve to the subsonic or supersonic branch
    Expected inputs:
    Po       : Stagnation pressure, Pa
    Rs       : Specific gas constant, J/kgK (double check units)
    To       : Stagnation temperature, K
    gamma    : Ratio of specific heats
    mdot     : Mass flow rate, kg/s
    Apipe    : Cross-sectional area of pipe, sq. meters
    subsuper : Specify either 'subsonic' or 'supersonic'

    Returns: M
    '''

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

    Returns: M
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


def aratio_from_mach(M, gamma):
    """
    Calculates the isentropic area ratio A/A* for a given Mach number and gamma.
    Expected inputs:
    M        : Mach number
    gamma    : Ratio of specific heats

    Returns: Aratio
    """
    term1 = 2 / (gamma + 1)
    term2 = 1 + (gamma - 1) / 2 * M**2
    exponent = (gamma + 1) / (2 * (gamma - 1))
    Aratio = (1 / M) * (term1 * term2) ** exponent
    return Aratio

def po_from_pratio(P,gamma,M):
    '''
    Function calculates the static pressure knowing the gas properties, Mach number, and stagnation pressure using the isentropic pressure ratio equation P/Po
    Expected inputs:
    Po       : Stagnation pressure, any units can be used. Static pressure will be returned in the same units provided for stagnation pressure
    gamma    : Ratio of specific heats
    M        : Mach number

    Returns: Po
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

    Returns: P_static
    '''
    P_static = Po*(1+((gamma-1)/2)*M**2)**(-(gamma)/(gamma-1))
    return P_static

def T_from_Tratio(To,gamma,M):
    '''
    Function calculates the static temperature knowing the gas properties, Mach number, and stagnation temperature using the isentropic temperature ratio equation P/Po
    Expected inputs:
    To       : Stagnation temperature, K
    gamma    : Ratio of specific heats
    M        : Mach number
    
    Returns: T_static

    '''
    return To/(1+((gamma-1)/2)*M**2)

def To_from_Tratio(T,gamma,M):
    '''
    Function calculates the static temperature knowing the gas properties, Mach number, and stagnation temperature using the isentropic temperature ratio equation P/Po
    Expected inputs:
    T       : Stagnation temperature, K
    gamma    : Ratio of specific heats
    M        : Mach number

    Returns: To

    '''
    return T*(1+((gamma-1)/2)*M**2)

##############################################
#              WRAPPED EQUATIONS             #
##############################################


def delta_mass_static(M,mdot,P,Rs,To,gamma,A):
    '''
    Using the mdot over astar equation for choked flow combined with the P/Po equation, provides an equation to iterate on knowing all other parameters.
    Expected inputs:
    M        : Mach number of the flow
    mdot     : Mass flow rate, kg/s
    P        : Static pressure, Pa
    Rs       : Specific gas constant, J/kgK (double check units)
    To       : Stagnation temperature, K
    gamma    : Ratio of specific heats
    A        : Cross-sectional area of the pipe in sq. m
    '''

    return mdot - P*(1+(gamma-1)/2*M*M)**(gamma/(gamma-1))*A*np.sqrt(gamma/(Rs*To))*M*(1+(gamma-1)/2*M*M)**(-(gamma+1)/(2*(gamma-1)))


