# CompressibleFlowFunctions

A library of gas dynamic equations for compressible flow, organized into submodules:
- [`Isentropic.py`](docs/Isentropic.md): Isentropic flow relations
- [`NSW.py`](docs/NSW.md): Normal shock equations
- [`Fanno.py`](docs/Fanno.md): Fanno flow relations
- [`Expansion.py`](docs/Expansion.md): Prandtl-Meyer equations
- [`misc.py`](docs/misc.md): General flow calculations (valve coefficients, unit conversions, etc.)


## Installation

As the maintainer, you can install the package locally using:

```sh
python setup.py install
```

Or, for editable/development mode:

```sh
pip install -e .
```

## Import

```python
from CompressibleFlowFunctions.Isentropic import *
```

