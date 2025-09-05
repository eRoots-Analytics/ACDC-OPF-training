import os
import VeraGridEngine as gce

fname = os.path.join('..', 'data', 'pglib_opf', 'pglib_opf_case14_ieee.m')
main_circuit = gce.open_file(fname)

# declare the snapshot opf
opf_options = gce.OptimalPowerFlowOptions(solver=gce.SolverType.NONLINEAR_OPF,
                                          ips_tolerance=1e-6,
                                          ips_iterations=40)
opf_driver = gce.OptimalPowerFlowDriver(grid=main_circuit, options=opf_options)
opf_driver.run()

opf_res: gce.OptimalPowerFlowResults = opf_driver.results
print("Buses:\n", opf_res.get_bus_df())
print("Generators:\n", opf_res.get_gen_df())
print("Branches:\n", opf_res.get_branch_df())
