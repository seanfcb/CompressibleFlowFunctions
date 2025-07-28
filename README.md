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

## GUI

The GUI provides an interactive interface for all major functions in the library:

- **Module Selection:** Choose from Isentropic, Fanno, NSW, Expansion, or Misc modules.
- **Function Selection:** After selecting a module, pick a function to use from a dropdown menu.
- **Argument Entry:** The GUI displays all required arguments for the selected function, including units and a brief description.
- **Calculation:** Enter your values and click "Run" to see the result instantly in the output box.
- **No Coding Required:** All calculations can be performed without writing any code.

This tool is ideal for quick engineering calculations, exploring the library’s capabilities, or verifying results without leaving a graphical environment. To run:
```python
python CompressibleFlowFunctions_GUI.py
```
or simply run the script in your favourite IDE.
