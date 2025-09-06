import os
import VeraGridEngine as vg

fname = os.path.join('..', 'data', 'pglib_opf', 'pglib_opf_case14_ieee.m')
grid = vg.open_file(fname)

# declare the snapshot opf
opf_options = vg.OptimalPowerFlowOptions(solver=vg.SolverType.NONLINEAR_OPF,
                                         ips_tolerance=1e-6,
                                         ips_iterations=40)
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
