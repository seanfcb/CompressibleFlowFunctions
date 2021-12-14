import numpy as np
import sys
from scipy.optimize import *
from CompressibleFlowFunctions.Isentropic import *
from CompressibleFlowFunctions.Fanno import *
from CompressibleFlowFunctions.NSW import *
from CompressibleFlowFunctions.misc import *


###All functions take as an input: pressure in PSI, Temperature in Kelvin, Pipe diameters in inches
###All functions output answers in SI units

def fanno_losses_backwards(Po2,To,gamma,M2,Rs,Dpipe,mu,epsilon,L,fluid): #function to be added to CompressibleFlowFunctions.py
    '''
    Function calculates initial conditions in a friction pipe knowing the exit conditions
    Expected inputs:
    Po2      : Exit Stagnation pressure, PSI
    To       : Stagnation temperature, K
    gamma    : Ratio of specific heats
    M2       : Exit Mach number
    Rs       : Specific gas constant, J/kgK (double check units)
    Dpipe    : Pipe diameter, meters
    mu       : Dynamic viscosity
    epsilon  : Surface roughness
    L        : Pipe length, meters
    '''
    PHI2           = fanno_equation(M2,gamma)
    f, Re          = fanning_and_reynolds(Po2,To,gamma,M2,Rs,Dpipe,mu,epsilon,fluid)
    Lstar2         = Lstar_fanno(f,Dpipe,M2,gamma)
    fanno_constant = 4*f*L/Dpipe
    PHI1           = fanno_constant + PHI2
    Lstar1         = Lstar2 + L
    M1             = bisect(delta_fanno,0.001,0.9999,args=(Lstar1,f,Dpipe,gamma))
    Poratf  = fanno_po_ratio(M2,gamma)
    Postar  = Po2/Poratf
    Po1     = Postar*fanno_po_ratio(M1,gamma)
    P1      = p_from_pratio(Po1,gamma,M1)
    P2      = p_from_pratio(Po2,gamma,M2)

    return M1, Po1, P1, Po2, P2, Lstar1, Lstar2


def valve_losses_backwards(P1,Cv,SG,Q,mdot,Rs,To,gamma,Apipe): ##Based on the deltrol equation
    P_bval  = newton(flowrates_backwards,P1, args=(P1,Cv,SG,Q))
    if P_bval > 2*P1:
        P_bval = flowrates_choked(Cv,SG,Q)
    M_bval  = bisect(delta_mass_static,0.0000001,0.99999999,args=(mdot,P_bval*101325/14.7,Rs,To,gamma,Apipe))
    #Po_bval = P_bval/(1+((gamma-1)/2)*M_bval**2)**(-(gamma)/(gamma-1))
    Po_bval = po_from_pratio(P_bval,gamma,M_bval)
    return P_bval, Po_bval, M_bval

# def valve_losses_backwards(P2,Cv,SG,Q,mdot,Rs,To,gamma,Apipe): ##Based on the Swagelok equation
#     '''
#     Does this display anything
#
#     '''
#     def delmass(Po,M,mdot,Rs,To,gamma,A):
#         return delta_mass_stag(M,mdot,Po,Rs,To,gamma,A)
#     def find_P_bval(P1,P2,Cv,SG,Q,mdot,Rs,To,gamma,Apipe):
#         T1   = newton(flowrates_swagelok,To-10,args=(P2,P1,Cv,SG,Q))
#         M1   = newton(mach_from_Tratio,0.2,args=(To,T1,gamma))
#         Po1a = po_from_pratio(P1,gamma,M1)
#         Po1b = newton(delmass,Po1a*101325/14.7,args=(M1,mdot,Rs,To,gamma,Apipe))
#         return Po1a - Po1b
#
#     P_bval = newton(find_P_bval,P2+10,args=(P2,Cv,SG,Q,mdot,Rs,To,gamma,Apipe))
#
#     return P_bval#, Po_bval, M_bval



def fanno_losses(mdot,Rs,SG,Dpipe,Apipe,Po1,Po1_metric,To,gamma,mu,epsilon,L):
    ##==================================================================##
    ##============================PART 1================================##
    ##==================================================================##
    #Calculate the Mach number at the inlet of the pipe.
    ##==================================================================##
    M1  = bisect(delta_mass_stag,0.0001,0.99,args=(mdot,Po1_metric,Rs,To,gamma,Apipe))
    ##==================================================================##
    #Calculate the Fanning friction factor
    ##==================================================================##
    P1         = p_from_pratio(Po1,gamma,M1)
    fanning, Re = fanning_and_reynolds(Po1,To,gamma,M1,Rs,Dpipe,mu,epsilon)



    ##==================================================================##
    #Check that PHI(M1) > 4fL/D and calculate PHI(M2) if possible
    ##==================================================================##
    fanno_constant = 4*fanning*L/Dpipe
    PHI1           = fanno_equation(M1,gamma)
    if PHI1 < fanno_constant:
        sys.exit("This pipe will choke before the next flow device")
    else:
        PHI2 = PHI1 - fanno_constant

    ##==================================================================##
    #Calculate Po2/Po1 using 2.3
    #Return Po2 & M2
    ##==================================================================##
    Lstar1   = Lstar_fanno(fanning,Dpipe,M1,gamma)
    L_int   = Lstar1 - L
    M2      = mach_fanno(L_int,fanning,Dpipe,gamma)
    Poratf  = fanno_po_ratio(M1,gamma)
    Postar  = Po1/Poratf
    Po2     = Postar*fanno_po_ratio(M2,gamma)
    P2      = p_from_pratio(Po2,gamma,M2)

    return P1, Po1, M1, Lstar1, P2, Po2, M2, Re

def valve_losses(P1,Cv,SG,Q,mdot,Rs,To,gamma,Apipe):
    #P2 = bisect(flowrates, 0, P1,args=(P1,Cv,SG,Q))
    P2 = bisect(flowrates,0,P1,args=(P1,Cv,SG,Q))
    M_aval  = bisect(delta_mass_static,0.0001,0.99,args=(mdot,P2*101325/14.7,Rs,To,gamma,Apipe))
    Po_aval = P2/(1+((gamma-1)/2)*M_aval**2)**(-(gamma)/(gamma-1))
    return P2,M_aval,Po_aval
