# misc.py Functions

| Function | Description | Inputs | Returns |
|----------|-------------|--------|---------|
| `flowrates(P2, P1, Cv, SG, Q)` | Calculates the static pressure drop through a flow device rated by Cv. | - `P1`: Upstream pressure (PSI)<br>- `P2`: Downstream pressure (PSI)<br>- `Cv`: Flow coefficient<br>- `SG`: Specific gravity (relative to air)<br>- `Q`: Volumetric flow rate (SCFH) | Pressure drop equation residual |
| `fanning_and_reynolds(Po1, To, gamma, M, Rs, Dpipe, mu, epsilon, fluid)` | Calculates Fanning friction factor and Reynolds number for a given flow. | - `Po1`: Stagnation pressure (Pa)<br>- `To`: Stagnation temperature (K)<br>- `gamma`: Ratio of specific heats<br>- `M`: Mach number<br>- `Rs`: Specific gas constant (J/kg·K)<br>- `Dpipe`: Pipe diameter (m)<br>- `mu`: Dynamic viscosity (Pa·s)<br>- `epsilon`: Pipe roughness (m)<br>- `fluid`: Fluid name (e.g., `'oxygen'`, `'hydrogen'`) | `fanning`: Fanning friction factor<br>`Re`: Reynolds number |
| `flowrates_choked(Cv, SG, Q)` | Calculates the static pressure drop through a choked flow device rated by Cv. | - `Cv`: Flow coefficient<br>- `SG`: Specific gravity (relative to air)<br>- `Q`: Volumetric flow rate (SCFH) | Pressure drop equation residual |
| `flowrates_backwards(P1, P2, Cv, SG, Q)` | Iterates on inlet pressure for a given flow device and conditions. | - `P1`: Upstream pressure (PSI)<br>- `P2`: Downstream pressure (PSI)<br>- `Cv`: Flow coefficient<br>- `SG`: Specific gravity (relative to air)<br>- `Q`: Volumetric flow rate (SCFH) | Inlet pressure (PSI) |
| `mdot_to_scfh(mdot, Rs, G)` | Converts mass flow rate to standard cubic feet per hour (SCFH) for Nitrogen. | - `mdot`: Mass flow rate (g/s)<br>- `Rs`: Specific gas constant (J/kg·K)<br>- `G`: Specific gravity of the fluid | `scfh`: Volumetric flow rate (SCFH) |
| `hole_numbers(Dhole, Astar)` | Calculates the number of injector holes given choking area and drill diameter. | - `Dhole`: Hole diameter (units compatible with `Astar`)<br>- `Astar`: Choking area (units compatible with `Dhole`) | `numholes`: Number of holes |

---

## Example Usage

```python
from CompressibleFlowFunctions.misc import *

scfh = mdot_to_scfh(mdot=10, Rs=296.8, G=0.97)
print("Volumetric flow rate (SCFH):", scfh)

fanning, Re = fanning_and_reynolds(Po1=101325, To=300, gamma=1.4, M=2.0, Rs=287, Dpipe=0.05, mu=1.8e-5, epsilon=1e-6, fluid='oxygen')
print("Fanning friction factor:", fanning)
print("Reynolds number:", Re)