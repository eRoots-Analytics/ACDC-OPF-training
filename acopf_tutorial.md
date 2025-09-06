# Nonlinear Optimal Power Flow (AC-OPF) tutorial

The non-linear optimal power flow is a power flow optimization with equality and innequality constraints.

You can think of it as a power flow with dispatching capabilities.

## A bit o theory

$$
min:  f(x)
$$
s.t. 
$$
g(x) = 0
$$
$$
h(x) \geq 0
$$

- $f(x)$: is the objective function.
- $g(x)$: collection of equality functions.
- $h(x)$: collection of inequality functions.

The main electrotechnical equation to solve is the power flow equation:

$$
S = V \cdot (Y \times V)*
$$

- $S$: Vector of power flow injections
- $V$: Vector of nodal voltages
- $Y$: Matrix of branch and shunt admittances

Analogously, we can get the passive branch flows like

$$
	S_f = {Vm_f^2} \cdot {y_{ff}}^{*} + Vm_f^{\angle{\theta_f}} \cdot Vm_t^{\angle{-\theta_t}}  \cdot {y_{ft}}^{*}
$$

$$
	S_t = {Vm_t^2} \cdot {y_{tt}}^{*} + Vm_f^{\angle{-\theta_f}} \cdot Vm_t^{\angle{\theta_t}}  \cdot {y_{tf}}^{*}
$$

Where, the admittance primitives are:

$$
	y_{ff} = \frac{ys + ysh}{m^2 \cdot m_f^2  \cdot e ^{j \cdot 2\tau} }
$$

$$
	y_{ft} = \frac{-ys}{m  \cdot m_f \cdot m_t} 
$$

$$
	y_{tf} = \frac{-ys}{m \cdot m_f \cdot m_t  \cdot e ^{j \cdot 2\tau} } 
$$

$$
	y_{tt} = \frac{ys + ysh}{m_t^2} 
$$


The transformer taps^

# Important parameters


## 4 bus grid from scratch


```python
import VeraGridEngine as vg

# Grid instantiation
grid = vg.MultiCircuit()

# Define buses
bus1 = grid.add_bus(vg.Bus(name='B1', Vnom=135, is_slack=True))
bus2 = grid.add_bus(vg.Bus(name='B2', Vnom=135))
bus5 = grid.add_bus(vg.Bus(name='B5', Vnom=135))
bus6 = grid.add_bus(vg.Bus(name='B6', Vnom=135))

# Define AC lines
line12 = grid.add_line(vg.Line(name='L12', bus_from=bus1, bus_to=bus2, r=0.001, x=0.01, rate=12))
line25 = grid.add_line(vg.Line(name='L25', bus_from=bus2, bus_to=bus5, r=0.05, x=0.05, rate=12))
line56 = grid.add_line(vg.Line(name='L56', bus_from=bus5, bus_to=bus6, r=0.001, x=0.01, rate=12))
line256 = grid.add_line(vg.Line(name='L562', bus_from=bus5, bus_to=bus6, r=0.001, x=0.01, rate=12))

# Define Hvdc Line
line34 = grid.add_hvdc(vg.HvdcLine(name='HVDC34', bus_from=bus2, bus_to=bus5, Pset=0.2, rate=120))

# Define generators
grid.add_generator(bus=bus1, api_obj=vg.Generator(name='Gen1', P=1.0, vset=1.01))
grid.add_generator(bus=bus6, api_obj=vg.Generator(name='Gen2', P=1.0, vset=1.02))

# Define loads
grid.add_load(bus=bus2, api_obj=vg.Load(name='Load1', P=3.0, Q=0.3))
grid.add_load(bus=bus5, api_obj=vg.Load(name='Load2', P=2.0, Q=0.5))

# declare the snapshot opf
opf_options = vg.OptimalPowerFlowOptions(solver=vg.SolverType.NONLINEAR_OPF,
                                         ips_tolerance=1e-6,
                                         ips_iterations=40,
                                         ips_trust_radius=1.0,
                                         ips_init_with_pf=False,
                                         ips_control_q_limits=False,
                                         acopf_mode=vg.AcOpfMode.ACOPFstd,
                                         acopf_v0=None,
                                         acopf_S0=None)
opf_driver = vg.OptimalPowerFlowDriver(grid=grid, options=opf_options)
opf_driver.run()

opf_res: vg.OptimalPowerFlowResults = opf_driver.results
print("Buses:\n", opf_res.get_bus_df())
print("Generators:\n", opf_res.get_gen_df())
print("Branches:\n", opf_res.get_branch_df())
print("HvdcLines:\n", opf_res.get_hvdc_df())
print("error: ", opf_res.error)
```


## IEEE 14 OPF case

```python
import os
import VeraGridEngine as vg

fname = os.path.join('..', 'data', 'pglib_opf', 'pglib_opf_case14_ieee.m')
grid = vg.open_file(fname)

# declare the snapshot opf
opf_options = vg.OptimalPowerFlowOptions(solver=vg.SolverType.NONLINEAR_OPF,
                                         ips_tolerance=1e-6,
                                         ips_iterations=40,
                                         ips_trust_radius=1.0,
                                         ips_init_with_pf=False,
                                         ips_control_q_limits=False,
                                         acopf_mode=vg.AcOpfMode.ACOPFstd,
                                         acopf_v0=None,
                                         acopf_S0=None)
opf_driver = vg.OptimalPowerFlowDriver(grid=grid, options=opf_options)
opf_driver.run()

opf_res: vg.OptimalPowerFlowResults = opf_driver.results
print("Buses:\n", opf_res.get_bus_df())
print("Generators:\n", opf_res.get_gen_df())
print("Branches:\n", opf_res.get_branch_df())
print("error: ", opf_res.error)

# -----------------------------------------------------------------------------
# Re run initializing with a power flow:
# -----------------------------------------------------------------------------

pf_res = vg.power_flow(grid)

# declare the snapshot opf
opf_options = vg.OptimalPowerFlowOptions(solver=vg.SolverType.NONLINEAR_OPF,
                                         ips_tolerance=1e-6,
                                         ips_iterations=40,
                                         ips_trust_radius=1.0,
                                         ips_init_with_pf=False,
                                         ips_control_q_limits=True,
                                         acopf_mode=vg.AcOpfMode.ACOPFstd,
                                         acopf_v0=pf_res.voltage,
                                         acopf_S0=pf_res.Sbus)
opf_driver = vg.OptimalPowerFlowDriver(grid=grid, options=opf_options)
opf_driver.run()

opf_res: vg.OptimalPowerFlowResults = opf_driver.results
print("Buses:\n", opf_res.get_bus_df())
print("Generators:\n", opf_res.get_gen_df())
print("Branches:\n", opf_res.get_branch_df())
print("error: ", opf_res.error)
```

