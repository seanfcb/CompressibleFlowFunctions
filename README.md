# CompressibleFlowFunctions

A library of gas dynamic equations for compressible flow, organized into submodules:
- [`Isentropic.py`](docs/Isentropic.md): Isentropic flow relations
- [`NSW.py`](docs/NSW.md): Normal shock equations
- [`Fanno.py`](docs/Fanno.md): Fanno flow relations
- [`Expansion.py`](docs/Expansion.md): Prandtl-Meyer equations
- [`misc.py`](docs/misc.md): General flow calculations (valve coefficients, unit conversions, etc.)
- [`geometry.py`](docs/geometry.md): Geometric calculations (surface areas, volumes, etc.)


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
from CompressibleFlowFunctions.NSW import *
from CompressibleFlowFunctions.Fanno import *
from CompressibleFlowFunctions.Expansion import *
from CompressibleFlowFunctions.misc import *
from CompressibleFlowFunctions.geometry import *
```

## GUI

A script in the library's main folder allows the user to make quick calculations without writing a full script or using ipython. To run:
```sh
python CompressibleFlowFunctions_GUI.py
```
or simply run the script in your favourite IDE.

The GUI provides an interactive interface for all major functions in the library:

- **Module Selection:** Choose from Isentropic, Fanno, NSW, Expansion, Misc, or Geometry modules.
- **Function Selection:** After selecting a module, pick a function to use from a dropdown menu.
- **Argument Entry:** The GUI displays all required arguments for the selected function, including units and a brief description.
- **Calculation:** Enter your values and click "Run" to see the result instantly in the output box.