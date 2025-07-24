# Fanno.py Functions

| Function | Description | Inputs | Returns |
|----------|-------------|--------|---------|
| `colebrook_white(f, Re, D, epsilon)` | Computes the Colebrook-White equation for Darcy friction factor (divide by 4 for Fanning friction factor). | - `f`: Darcy friction factor<br>- `Re`: Reynolds number<br>- `D`: Pipe diameter (m)<br>- `epsilon`: Surface roughness (μm) | Equation residual (for iteration) |
| `fanno_equation(M, gamma)` | Calculates the Fanno equation value for a given Mach number and gamma. | - `M`: Mach number<br>- `gamma`: Ratio of specific heats | Fanno equation value |
| `delta_fanno(M, L, f, D, gamma)` | Returns the difference between both sides of the Fanno equation (for root finding). | - `M`: Inlet Mach number<br>- `L`: Pipe length (m)<br>- `f`: Fanning friction factor<br>- `D`: Pipe diameter (m)<br>- `gamma`: Ratio of specific heats | Equation residual |
| `Lstar_fanno(f, D, M, gamma)` | Directly calculates the Fanno choking length \(L^*\) for given conditions. | - `f`: Fanning friction factor<br>- `D`: Pipe diameter (m)<br>- `M`: Inlet Mach number<br>- `gamma`: Ratio of specific heats | `Lstar`: Choking length (m) |
| `mach_fanno(L, f, D, gamma)` | Calculates Mach number for a given pipe length using the Fanno equation. | - `L`: Pipe length (m)<br>- `f`: Fanning friction factor<br>- `D`: Pipe diameter (m)<br>- `gamma`: Ratio of specific heats | `M`: Mach number |
| `fanno_po_ratio(M, gamma)` | Calculates the Fanno stagnation pressure ratio for a given Mach number and gamma. | - `M`: Mach number<br>- `gamma`: Ratio of specific heats | Stagnation pressure ratio |

---

## Example Usage

```python
from CompressibleFlowFunctions.Fanno import *

Lstar = Lstar_fanno(f=0.02, D=0.05, M=0.8, gamma=1.4)
print("Choking length:", Lstar)

M = mach_fanno(L=2.0, f=0.02, D=0.05, gamma=1.4)
print("Mach number:", M)
```

## Notes

- Use the Colebrook-White function with a root-finding algorithm to solve for friction factor.
- All lengths in meters, diameters in meters, and surface roughness in micrometers unless otherwise noted.
- Fanning friction factor is one-fourth the Darcy friction factor.