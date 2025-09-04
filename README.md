## ACDC-OPF-training
Hands-on Training on AC Optimal Power Flows and AC/DC Power Flows Through VeraGrid



# Introduction
This repository contains several scripts and markdown tutorials that can be used in conjunction with the VeraGrid GUI

- [ACDC Power Flow](acdc_power_flow.md)
- [AC Optimal Power Flow](acopf_tutorial.md)

# Requirements
- [Download Python](https://www.python.org/downloads/) 3.10-3.13 (3.12 recomended)
- Alternativelly, get a python distribution + all packages installed from [eroots.tech/software](https://www.eroots.tech/veragrid-download)

# Sofwtare installation

```shell
pip3 install veragrid
```

# Execution with user interface

From the terminal run `veragrid` to launch the graphical user interface.

For scripting, run as you normally would.

To launch the user interface from a script: 

```python
from VeraGrid.ExecuteVeraGrid import runVeraGrid

runVeraGrid()
```

or in a single line

```bash
python3`` -c "from VeraGrid.ExecuteVeraGrid import runVeraGrid;runVeraGrid()"
```