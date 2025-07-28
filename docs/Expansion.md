# Expansion.py Functions

| Function | Description | Inputs | Returns |
|----------|-------------|--------|---------|
| `prandtl_meyer(M, gamma)` | Calculates the Prandtl-Meyer expansion angle (ν) for a given Mach number and ratio of specific heats. | - `M`: Mach number<br>- `gamma`: Ratio of specific heats | `nu`: Prandtl-Meyer angle (radians) |
| `mach_angle(M)` | Calculates the Mach angle (μ) for a given Mach number. | - `M`: Mach number | `mu`: Mach angle (radians) |

---

## Example Usage

```python
from CompressibleFlowFunctions.Expansion import *

nu = prandtl_meyer(M=2.0, gamma=1.4)
print("Prandtl-Meyer angle (rad):", nu)

mu = mach_angle(M=2.0)
print("Mach angle (rad):", mu)
```

---

## Notes

- Angles are returned in radians. Use `np.degrees()` to convert to degrees if needed.
- `gamma` is typically 1.4 for air.
