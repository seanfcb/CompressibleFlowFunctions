# NSW.py Functions

| Function | Description | Inputs | Returns |
|----------|-------------|--------|---------|
| `prat_from_mach(gamma, M)` | Calculates the stagnation pressure ratio across a normal shock wave for a given pre-shock Mach number. | - `gamma`: Ratio of specific heats<br>- `M`: Mach number before shock | `pratio`: Stagnation pressure ratio |
| `mach_from_pressure_ratio(Po1, Po2, gamma)` | Calculates the pre-shock Mach number for a desired stagnation pressure ratio across a normal shock wave. | - `Po1`: Stagnation pressure before shock (any units)<br>- `Po2`: Stagnation pressure after shock (same units as Po1)<br>- `gamma`: Ratio of specific heats | `M`: Mach number before shock |
| `mach_after_shock(M1, gamma)` | Calculates the Mach number after a normal shock wave. | - `M1`: Mach number before shock<br>- `gamma`: Ratio of specific heats | `M2`: Mach number after shock |
| `pstatic_after_shock(M, gamma, P)` | Calculates the static pressure after a normal shock wave. | - `M`: Mach number before shock<br>- `gamma`: Ratio of specific heats<br>- `P`: Static pressure before shock (Pa) | `P2`: Static pressure after shock (Pa) |
| `pstag_after_shock(M, gamma, Po1)` | Calculates the stagnation pressure after a normal shock wave. | - `M`: Mach number before shock<br>- `gamma`: Ratio of specific heats<br>- `Po1`: Stagnation pressure before shock (Pa) | `Po2`: Stagnation pressure after shock (Pa) |

---

## Example Usage

```python
from CompressibleFlowFunctions.NSW import *

M2 = mach_after_shock(M1=2.5, gamma=1.4)
print("Mach number after shock:", M2)

P2 = pstatic_after_shock(M=2.5, gamma=1.4, P=101325)
print("Static pressure after shock:", P2)
```

---

## Notes

- All pressures should be in consistent units.
- These functions assume a normal shock wave (NSW) in one-dimensional flow.
- `gamma` is typically 1.4 for air.
