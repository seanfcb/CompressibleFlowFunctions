# Isentropic.py Functions

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

## Example Usage

```python
from CompressibleFlowFunctions.Isentropic import *

A_throat = throat_area_from_mdot(mdot=0.5, Po=101325, Rs=287, To=300, gamma=1.4)
print(A_throat)
```

---

## Notes

- All pressures and temperatures should be in SI units unless otherwise noted.
- Specify `'subsonic'` or `'supersonic'` for functions that resolve multiple branches.