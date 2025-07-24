# CompressibleFlowFunctions

A library of gas dynamic equations for compressible flow, organized into submodules:
- `Isentropic.py`: Isentropic flow relations
- `NSW.py`: Normal shock equations
- `Fanno.py`: Fanno flow relations
- `Expansion.py`: Prandtl-Meyer equations
- `misc.py`: General flow calculations (valve coefficients, unit conversions, etc.)

## Installation & Import

```python
from CompressibleFlowFunctions.Isentropic import *
```

---

## Isentropic.py Functions

| Function | Description | Inputs | Returns |
|----------|-------------|--------|---------|
| `throat_area_from_mdot(mdot, Po, Rs, To, gamma)` | Calculates the minimum (choked) area required for a given mass flow and stagnation conditions. | - `mdot`: Mass flow rate (kg/s)<br>- `Po`: Stagnation pressure (Pa)<br>- `Rs`: Specific gas constant (J/kg·K)<br>- `To`: Stagnation temperature (K)<br>- `gamma`: Ratio of specific heats | `A_throat`: Choked area (m²) |
| `astar_all_else_known(Apipe, M, gamma)` | Calculates choking area and diameter from area ratio and Mach number. | - `Apipe`: Pipe area (m²)<br>- `M`: Mach number<br>- `gamma`: Ratio of specific heats | `Astar`: Choked area (m²), `Dstar`: Choked diameter (m) |
| `mach_from_G(Po, Rs, To, gamma, mdot, Apipe, subsuper)` | Finds Mach number from flow properties; resolves subsonic/supersonic branch. | - `Po`: Stagnation pressure (Pa)<br>- `Rs`: Specific gas constant (J/kg·K)<br>- `To`: Stagnation temperature (K)<br>- `gamma`: Ratio of specific heats<br>- `mdot`: Mass flow rate (kg/s)<br>- `Apipe`: Pipe area (m²)<br>- `subsuper`: `'subsonic'` or `'supersonic'` | `M`: Mach number |
| `mach_from_aratio(Apipe, Astar, gamma, subsuper)` | Finds Mach number from area ratio; resolves subsonic/supersonic branch. | - `Apipe`: Pipe area (m²)<br>- `Astar`: Choked area (m²)<br>- `gamma`: Ratio of specific heats<br>- `subsuper`: `'subsonic'` or `'supersonic'` | `M`: Mach number |
| `aratio_from_mach(M, gamma)` | Calculates isentropic area ratio \(A/A^*\) for a given Mach number. | - `M`: Mach number<br>- `gamma`: Ratio of specific heats | `Aratio`: Area ratio |
| `po_from_pratio(P, gamma, M)` | Calculates stagnation pressure from static pressure and Mach number. | - `P`: Static pressure (Pa)<br>- `gamma`: Ratio of specific heats<br>- `M`: Mach number | `Po`: Stagnation pressure (Pa) |
| `p_from_pratio(Po, gamma, M)` | Calculates static pressure from stagnation pressure and Mach number. | - `Po`: Stagnation pressure (Pa)<br>- `gamma`: Ratio of specific heats<br>- `M`: Mach number | `P_static`: Static pressure (Pa) |
| `T_from_Tratio(To, gamma, M)` | Calculates static temperature from stagnation temperature and Mach number. | - `To`: Stagnation temperature (K)<br>- `gamma`: Ratio of specific heats<br>- `M`: Mach number | `T_static`: Static temperature (K) |
| `To_from_Tratio(T, gamma, M)` | Calculates stagnation temperature from static temperature and Mach number. | - `T`: Static temperature (K)<br>- `gamma`: Ratio of specific heats<br>- `M`: Mach number | `To`: Stagnation temperature (K) |
| `delta_mass_static(M, mdot, P, Rs, To, gamma, A)` | Iterative equation for choked flow using mass flow and static pressure. | - `M`: Mach number<br>- `mdot`: Mass flow rate (kg/s)<br>- `P`: Static pressure (Pa)<br>- `Rs`: Specific gas constant (J/kg·K)<br>- `To`: Stagnation temperature (K)<br>- `gamma`: Ratio of specific heats<br>- `A`: Pipe area (m²) | — |

---

### Example Usage

```python
from CompressibleFlowFunctions.Isentropic import *

A_throat = throat_area_from_mdot(mdot=0.5, Po=101325, Rs=287, To=300, gamma=1.4)
print(A_throat)
```

---

### Notes

- All pressures and temperatures should be in SI units unless otherwise noted.
- Specify `'subsonic'` or `'supersonic'` for functions that resolve multiple branches.

---

For details on other submodules (`NSW.py`, `Fanno.py`, `Expansion.py`, `misc.py`), see their respective documentation sections.



## Fanno.py Functions

| Function | Description | Inputs | Returns |
|----------|-------------|--------|---------|
| `colebrook_white(f, Re, D, epsilon)` | Computes the Colebrook-White equation for Darcy friction factor (divide by 4 for Fanning friction factor). | - `f`: Darcy friction factor<br>- `Re`: Reynolds number<br>- `D`: Pipe diameter (m)<br>- `epsilon`: Surface roughness (μm) | Equation residual (for iteration) |
| `fanno_equation(M, gamma)` | Calculates the Fanno equation value for a given Mach number and gamma. | - `M`: Mach number<br>- `gamma`: Ratio of specific heats | Fanno equation value |
| `delta_fanno(M, L, f, D, gamma)` | Returns the difference between both sides of the Fanno equation (for root finding). | - `M`: Inlet Mach number<br>- `L`: Pipe length (m)<br>- `f`: Fanning friction factor<br>- `D`: Pipe diameter (m)<br>- `gamma`: Ratio of specific heats | Equation residual |
| `Lstar_fanno(f, D, M, gamma)` | Directly calculates the Fanno choking length \(L^*\) for given conditions. | - `f`: Fanning friction factor<br>- `D`: Pipe diameter (m)<br>- `M`: Inlet Mach number<br>- `gamma`: Ratio of specific heats | `Lstar`: Choking length (m) |
| `mach_fanno(L, f, D, gamma)` | Calculates Mach number for a given pipe length using the Fanno equation. | - `L`: Pipe length (m)<br>- `f`: Fanning friction factor<br>- `D`: Pipe diameter (m)<br>- `gamma`: Ratio of specific heats | `M`: Mach number |
| `fanno_po_ratio(M, gamma)` | Calculates the Fanno stagnation pressure ratio for a given Mach number and gamma. | - `M`: Mach number<br>- `gamma`: Ratio of specific heats | Stagnation pressure ratio |

---

### Example Usage

```python
from CompressibleFlowFunctions.Fanno import *

Lstar = Lstar_fanno(f=0.02, D=0.05, M=0.8, gamma=1.4)
print("Choking length:", Lstar)

M = mach_fanno(L=2.0, f=0.02, D=0.05, gamma=1.4)
print("Mach number:", M)
```

---

### Notes

- Use the Colebrook-White function with a root-finding algorithm to solve for friction factor.
- All lengths in meters, diameters in meters, and surface roughness in micrometers unless otherwise noted.
- Fanning friction factor is one-fourth the Darcy friction factor.

---


## NSW.py Functions

| Function | Description | Inputs | Returns |
|----------|-------------|--------|---------|
| `prat_from_mach(gamma, M)` | Calculates the stagnation pressure ratio across a normal shock wave for a given pre-shock Mach number. | - `gamma`: Ratio of specific heats<br>- `M`: Mach number before shock | `pratio`: Stagnation pressure ratio |
| `mach_from_pressure_ratio(Po1, Po2, gamma)` | Calculates the pre-shock Mach number for a desired stagnation pressure ratio across a normal shock wave. | - `Po1`: Stagnation pressure before shock (any units)<br>- `Po2`: Stagnation pressure after shock (same units as Po1)<br>- `gamma`: Ratio of specific heats | `M`: Mach number before shock |
| `mach_after_shock(M1, gamma)` | Calculates the Mach number after a normal shock wave. | - `M1`: Mach number before shock<br>- `gamma`: Ratio of specific heats | `M2`: Mach number after shock |
| `pstatic_after_shock(M, gamma, P)` | Calculates the static pressure after a normal shock wave. | - `M`: Mach number before shock<br>- `gamma`: Ratio of specific heats<br>- `P`: Static pressure before shock (Pa) | `P2`: Static pressure after shock (Pa) |
| `pstag_after_shock(M, gamma, Po1)` | Calculates the stagnation pressure after a normal shock wave. | - `M`: Mach number before shock<br>- `gamma`: Ratio of specific heats<br>- `Po1`: Stagnation pressure before shock (Pa) | `Po2`: Stagnation pressure after shock (Pa) |

---

### Example Usage

```python
from CompressibleFlowFunctions.NSW import *

M2 = mach_after_shock(M1=2.5, gamma=1.4)
print("Mach number after shock:", M2)

P2 = pstatic_after_shock(M=2.5, gamma=1.4, P=101325)
print("Static pressure after shock:", P2)
```

---

### Notes

- All pressures should be in consistent units.
- These functions assume a normal shock wave (NSW) in one-dimensional flow.
- `gamma` is typically 1.4 for air.

---

## Expansion.py Functions

| Function | Description | Inputs | Returns |
|----------|-------------|--------|---------|
| `prandtl_meyer(M, gamma)` | Calculates the Prandtl-Meyer expansion angle (ν) for a given Mach number and ratio of specific heats. | - `M`: Mach number<br>- `gamma`: Ratio of specific heats | `nu`: Prandtl-Meyer angle (radians) |
| `mach_angle(M)` | Calculates the Mach angle (μ) for a given Mach number. | - `M`: Mach number | `mu`: Mach angle (radians) |

---

### Example Usage

```python
from CompressibleFlowFunctions.Expansion import *

nu = prandtl_meyer(M=2.0, gamma=1.4)
print("Prandtl-Meyer angle (rad):", nu)

mu = mach_angle(M=2.0)
print("Mach angle (rad):", mu)
```

---

### Notes

- Angles are returned in radians. Use `np.degrees()` to convert to degrees if needed.
- `gamma` is typically 1.4 for air.

---

## misc.py Functions

| Function | Description | Inputs | Returns |
|----------|-------------|--------|---------|
| `flowrates(P2, P1, Cv, SG, Q)` | Calculates the static pressure drop through a flow device rated by Cv. | - `P1`: Upstream pressure (PSI)<br>- `P2`: Downstream pressure (PSI)<br>- `Cv`: Flow coefficient<br>- `SG`: Specific gravity (relative to air)<br>- `Q`: Volumetric flow rate (SCFH) | Pressure drop equation residual |
| `fanning_and_reynolds(Po1, To, gamma, M, Rs, Dpipe, mu, epsilon, fluid)` | Calculates Fanning friction factor and Reynolds number for a given flow. | - `Po1`: Stagnation pressure (Pa)<br>- `To`: Stagnation temperature (K)<br>- `gamma`: Ratio of specific heats<br>- `M`: Mach number<br>- `Rs`: Specific gas constant (J/kg·K)<br>- `Dpipe`: Pipe diameter (m)<br>- `mu`: Dynamic viscosity (Pa·s)<br>- `epsilon`: Pipe roughness (m)<br>- `fluid`: Fluid name (e.g., `'oxygen'`, `'hydrogen'`) | `fanning`: Fanning friction factor<br>`Re`: Reynolds number |
| `flowrates_choked(Cv, SG, Q)` | Calculates the static pressure drop through a choked flow device rated by Cv. | - `Cv`: Flow coefficient<br>- `SG`: Specific gravity (relative to air)<br>- `Q`: Volumetric flow rate (SCFH) | Pressure drop equation residual |
| `flowrates_backwards(P1, P2, Cv, SG, Q)` | Iterates on inlet pressure for a given flow device and conditions. | - `P1`: Upstream pressure (PSI)<br>- `P2`: Downstream pressure (PSI)<br>- `Cv`: Flow coefficient<br>- `SG`: Specific gravity (relative to air)<br>- `Q`: Volumetric flow rate (SCFH) | Inlet pressure (PSI) |
| `mdot_to_scfh(mdot, Rs, G)` | Converts mass flow rate to standard cubic feet per hour (SCFH) for Nitrogen. | - `mdot`: Mass flow rate (g/s)<br>- `Rs`: Specific gas constant (J/kg·K)<br>- `G`: Specific gravity of the fluid | `scfh`: Volumetric flow rate (SCFH) |
| `hole_numbers(Dhole, Astar)` | Calculates the number of injector holes given choking area and drill diameter. | - `Dhole`: Hole diameter (units compatible with `Astar`)<br>- `Astar`: Choking area (units compatible with `Dhole`) | `numholes`: Number of holes |

---

### Example Usage

```python
from CompressibleFlowFunctions.misc import *

scfh = mdot_to_scfh(mdot=10, Rs=296.8, G=0.97)
print("Volumetric flow rate (SCFH):", scfh)

fanning, Re = fanning_and_reynolds(Po1=101325, To=300, gamma=1.4, M=2.0, Rs=287, Dpipe=0.05, mu=1.8e-5, epsilon=1e-6, fluid='oxygen')
print("Fanning friction factor:", fanning)
print("Reynolds number:", Re)
```

---


