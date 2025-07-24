# CompressibleFlowFunctions

This is a library of gas dynamic equations built to provide users with the basic equations of compressible flow. This library is separated into 4 main sublibraries: 
- Isentropic.py for isentropic flow relations
- NSW.py for normal shock equations
- Fanno.py for Fanno flow relations
- Expansion.py for Prandtl-Meyer equations

A secondary sublibrary (misc.py) is also available and contains more general flow related calculations such as valve coefficient (Cv) calculations and unit conversions.

## Isentropic.py

To import, use:
```
from CompressibleFlowFunctions.Isentropic import *
```

### Available Functions
```
throat_area_from_mdot(mdot,Po,Rs,To,gamma)
```
Using the mdot over astar equation for choked flow, calculate choke area knowing all other properties.
Expected inputs:
- M        : Mach number of the flow
- mdot     : Mass flow rate, kg/s
- Po       : Stagnation pressure, Pa
- Rs       : Specific gas constant, J/kgK (double check units)
- To       : Stagnation temperature, K
- gamma    : Ratio of specific heats
- A        : Cross-sectional area of the pipe in sq. m

Returns: A_throat
```
astar_all_else_known(Apipe,M,gamma):
```
Function calculates the choking area (and diameter) using the compressible area ratio knowing all other properties
Expected inputs:
- Apipe    : Pipe cross sectional area, sq. m
- M        : Mach number
- gamma    : Ratio of specific heats

    - Returns: Astar, Dstar

```
mach_from_G(Po,Rs,To,gamma,mdot,Apipe,subsuper)
```
Calculates the Mach number knowing all other flow properties. This function allows the user to specify whether to resolve to the subsonic or supersonic branch
Expected inputs:
- Po       : Stagnation pressure, Pa
- Rs       : Specific gas constant, J/kgK (double check units)
- To       : Stagnation temperature, K
- gamma    : Ratio of specific heats
- mdot     : Mass flow rate, kg/s
- Apipe    : Cross-sectional area of pipe, sq. meters
- subsuper : Specify either 'subsonic' or 'supersonic'
- Returns: M

```
mach_from_aratio(Apipe,Astar,gamma,subsuper)
```
Function calculates the Mach number at a given location using the compressible area ratio knowing all other properties
Expected inputs:
- Apipe    : Pipe area, sq. m
- Astar    : Choking area, sq. m
- gamma    : Ratio of specific heats
- subsuper : Specify either 'subsonic' or 'supersonic'
- Returns: M

```
aratio_from_mach(M, gamma)
```
Calculates the isentropic area ratio A/A* for a given Mach number and gamma.
Expected inputs:
- M        : Mach number
- gamma    : Ratio of specific heats
- Returns: Aratio

```
po_from_pratio(P,gamma,M)
```
Function calculates the static pressure knowing the gas properties, Mach number, and stagnation pressure using the isentropic pressure ratio equation P/Po
Expected inputs:
- Po       : Stagnation pressure, any units can be used. Static pressure will be returned in the same units provided for stagnation pressure
- gamma    : Ratio of specific heats
- M        : Mach number
- Returns: Po

```
p_from_pratio(Po,gamma,M)
```
Function calculates the static pressure knowing the gas properties, Mach number, and stagnation pressure using the isentropic pressure ratio equation P/Po
Expected inputs:
- Po       : Stagnation pressure, any units can be used. Static pressure will be returned in the same units provided for stagnation pressure
- gamma    : Ratio of specific heats
- M        : Mach number
- Returns: P_static

```
T_from_Tratio(To,gamma,M)
```
Function calculates the static temperature knowing the gas properties, Mach number, and stagnation temperature using the isentropic temperature ratio equation P/Po
Expected inputs:
- To       : Stagnation temperature, K
- gamma    : Ratio of specific heats
- M        : Mach number
- Returns: T_static

```
To_from_Tratio(T,gamma,M)
```
Function calculates the static temperature knowing the gas properties, Mach number, and stagnation temperature using the isentropic temperature ratio equation P/Po
Expected inputs:
- T       : Stagnation temperature, K
- gamma    : Ratio of specific heats
- M        : Mach number
- Returns: To

### Wrapped functions
```
delta_mass_static(M,mdot,P,Rs,To,gamma,A)
```
 Using the mdot over astar equation for choked flow combined with the P/Po equation, provides an equation to iterate on knowing all other parameters.
Expected inputs:
- M        : Mach number of the flow
- mdot     : Mass flow rate, kg/s
- P        : Static pressure, Pa
- Rs       : Specific gas constant, J/kgK (double check units)
- To       : Stagnation temperature, K
- gamma    : Ratio of specific heats
- A        : Cross-sectional area of the pipe in sq. m











area_from_mass(Po,To,Rs,gamma,mdot): 

    ##Function calculates the choking area Astar using the compressible area ratio

mass_from_area(Po,To,Rs,gamma,Dpipe): 

    ##Function calculates the mass flow rate using the compressible area ratio m_dot/Astar

mach_from_pressure_ratio(Po1,Po2,gamma):
    ##For a desired stagnation pressure ratio, this function calculates the Mach number before a NSW using the normal shock equations

mach_after_shock(M1,gamma):

    ##Calculates the Mach number after a NSW knowing the pre-shock Mach number

pstatic_after_shock(M,gamma,P):

    ##Calculates the static pressure after a NSW knowing the pre-choke Mach number, gamma, and static pressure

pstag_after_shock(M,gamma,Po1):

    ##Calculates the stagnation pressure after a NSW knowing the pre-choke Mach number, gamma

astar_all_else_known(Dpipe,M,gamma):

    ##Function calculates the choking area using the compressible area ratio knowing all other properties
    
mach_from_aratio_subsonic(Aexit,Astar,gamma):

    ##Function calculates the Mach number at a given location using the compressible area ratio A/Astar knowing all other properties (areas, gamma)

mach_from_aratio_supersonic(Aexit,Astar,gamma):

    ##Function calculates the Mach number at a given location using the compressible area ratio knowing all other properties

aratio_from_mach(M,gamma):

    ##Function calculates the compressible area ratio A/Astar knowing the Mach number and gamma

p_from_pratio(Po,gamma,M):

    ##Function calculates the static pressure knowing the gas properties, Mach number, and stagnation pressure using the isentropic pressure ratio equation P/Po

hole_numbers(Dhole,Astar):

    ## Not part of the compressible flow solver per se, this function is used in injector design. 
    ## Once the choking area at the injector is known and using a specific hole diameter (drill bit size, etc.), this function spits out the number of holes required to choke.
