import numpy as np
import sys
from scipy.optimize import *
from CompressibleFlowFunctions.algos import *
from CompressibleFlowFunctions.Isentropic import *
from CompressibleFlowFunctions.Fanno import *
from CompressibleFlowFunctions.NSW import *

def flowrates(P2,P1,Cv,SG,Q):
    '''
    Calculates the static pressure drop through a flow device rated by Cv
    Expected inputs:
    P1 and P2: Pressures upstream and downstream, PSI
    Cv       : Flow coefficient
    SG       : Specific gravity w.r.t. air
    Q        : Volumetric flow rate, SCFH (see mdot_to_scfh)
    '''
    return 42.2*Cv*np.sqrt((P1-P2)*(P1+P2))/np.sqrt(SG) - Q
    # conv = 60*22.67*np.sqrt(5/9)#conversion constant
    # delP = P1-P2
    # return Q - conv*Cv*(1-(2/3)*delP/P1)*np.sqrt(delP/(P1*SG*T1))

def flowrates_swagelok(T1,P2,P1,Cv,SG,Q):
    '''
    Calculates the static pressure drop through a flow device rated by Cv
    Expected inputs:
    P1 and P2: Pressures upstream and downstream, PSI
    Cv       : Flow coefficient
    SG       : Specific gravity w.r.t. air
    Q        : Volumetric flow rate, SCFH (see mdot_to_scfh)
    '''
    conv = 60*22.67*np.sqrt(5/9)#conversion constant
    delP = P1-P2
    return Q - conv*Cv*(1-(2/3)*delP/P1)*np.sqrt(delP/(P1*SG*T1))

def flowrates_choked(Cv,SG,Q):
    '''
    Calculates the static pressure drop through a flow device rated by Cv
    Expected inputs:
    P1 and P2: Pressures upstream and downstream, PSI
    Cv       : Flow coefficient
    SG       : Specific gravity w.r.t. air
    Q        : Volumetric flow rate, SCFH (see mdot_to_scfh)
    '''
    return Q*np.sqrt(SG)/(42.2*0.87*Cv)
    # conv = 60*0.471*22.67*np.sqrt(5/9)
    # return Q*np.sqrt(SG*T1)/(conv*Cv)

def flowrates_backwards(P1,P2,Cv,SG,Q):
    '''
    Function simply wraps the flowrates() function to iterate on inlet pressure. Returns inlet pressure
    Expected inputs:
    P1 and P2: Pressures upstream and downstream, PSI
    Cv       : Flow coefficient
    SG       : Specific gravity w.r.t. air
    Q        : Volumetric flow rate, SCFH (see mdot_to_scfh)
    '''
    return flowrates(P2,P1,Cv,SG,Q)

def mdot_to_scfh(mdot,Rs,G):
    '''
    Function calculates the volumetric flow rate in standard cubic feet per hour (scfh) of Nitrogen.
    Expected inputs:
    mdot     : Mass flow rate, in g/s
    Rs       : Specific gas constant, J/kgK (double check units)
    G        : Specific gravity of the studied fluid
    '''
    mdot = mdot*60*2.205/1000 #g/s to lbm/min
    rho  = 101325/(Rs*288.7)*2.205/(3.28084**3) #calculate the stp density, converting to lb/cu.ft
    Q    = mdot/rho
    scfh = Q/np.sqrt(1/G)*60
    return scfh

def hole_numbers(Dhole,Astar):
    '''
    Function calculates the number of holes on an injector knowing the choking area Astar and the drill diameter.
    Expected inputs:
    Dhole    : Hole diameter. Units compatible with Astar
    Astar    : Choking area. Units compatible with Dhole
    '''
    numholes = 4*Astar/np.pi/Dhole/Dhole
    return numholes

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
