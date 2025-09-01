## ACDC-OPF-training
Hands-on Training on AC Optimal Power Flows and AC/DC Power Flows Through VeraGrid



# Introduction
This repository contains several scripts and notebooks that can be used in conjunction with the VeraGrid GUI

- ACDC PF Benchmarking with MatPower/MatACDC TODO: write the guide on how to set the controls for VSCs
- ACOPF Benchmarking with `https://lanl-ansi.github.io/PowerModels.jl/stable/power-flow/` TODO: cost/limits of gens

# Requirements
- Download Python 3.10-3.12
- Executable from [eroots.tech](https://www.eroots.tech/veragrid-download)

# Installation

```shell
pip3 install veragrid
```

# Execution

From the terminal run `veragrid` to launch the graphical user interface.

For scripting, run as you normally would.

To launch the user interface from a script: 

```python
from VeraGrid.ExecuteVeraGrid import runVeraGrid

runVeraGrid()
```