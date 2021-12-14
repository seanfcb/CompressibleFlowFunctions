import numpy as np
import sys
from scipy.optimize import *
from CompressibleFlowFunctions.Isentropic import *
from CompressibleFlowFunctions.Fanno import *
from CompressibleFlowFunctions.NSW import *
from CoolProp.CoolProp import PropsSI

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

# def flowrates_swagelok(T1,P2,P1,Cv,SG,Q):
#     '''
#     Calculates the static pressure drop through a flow device rated by Cv
#     Expected inputs:
#     P1 and P2: Pressures upstream and downstream, PSI
#     Cv       : Flow coefficient
#     SG       : Specific gravity w.r.t. air
#     Q        : Volumetric flow rate, SCFH (see mdot_to_scfh)
#     '''
#     conv = 60*22.67*np.sqrt(5/9)#conversion constant
#     delP = P1-P2
#     return Q - conv*Cv*(1-(2/3)*delP/P1)*np.sqrt(delP/(P1*SG*T1))


def fanning_and_reynolds(Po1,To,gamma,M,Rs,Dpipe,mu,epsilon,fluid):
    P1         = p_from_pratio(Po1,gamma,M)
    T1         = T_from_Tratio(To,gamma,M)
    rhoi       = P1*(101325/14.7)/(T1*Rs)
    if fluid == 'oxygen':
        mu = PropsSI('viscosity','T',T1,'P',P1*101.325/14.7,fluid)
    elif fluid == 'hydrogen':
        mu = PropsSI('viscosity','T',T1,'P',P1*101.325/14.7,fluid)

    Re         = rhoi*M*np.sqrt(gamma*Rs*T1)*Dpipe/mu
    darcy      = bisect(colebrook_white,1e-6,1,args=(Re,Dpipe,epsilon))
    fanning    = darcy/4

    return fanning, Re


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

def spacer_sizing(t,Po,To,Rs,mdot,gamma,specs):
    from CompressibleFlowFunctions.Isentropic import delta_mass_stag
    def delmass(A,M,mdot,Po,Rs,To,gamma):
        return delta_mass_stag(M,mdot,Po,Rs,To,gamma,A)

    dia     = specs[0] #Diameter used for choking calculations. Convert in to m
    alpha   = specs[1] #Angle of the injection surface on the pintle ring. MKII Ph2 alpha = 30deg.
    Astar1  = np.pi*(0.62*0.0254)**2/4
    #Astar1  = newton(delmass,0.001,args=(1,mdot,Po,Rs,To,gamma))
    Astar2  = np.pi*np.sin(alpha)*(dia+t*np.sin(alpha)*np.cos(alpha))*t
    #print(Astar1)
    return Astar1-Astar2
