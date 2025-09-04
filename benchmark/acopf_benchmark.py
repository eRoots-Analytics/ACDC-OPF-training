import os
from datetime import datetime
import pandas as pd
import VeraGridEngine as vge

folder = os.path.join('../data', 'pglib_opf')
data = dict()
total = 0
converged_count = 0
for name in os.listdir(folder):
    path = os.path.join(folder, name)
    if os.path.isfile(path) and name.lower().endswith(".m"):

        fname = os.path.join(folder, name)

        grid = vge.open_file(fname)

        # pf_options = vge.PowerFlowOptions(
        #     initialize_with_existing_solution=True
        # )
        # pf_drv = vge.PowerFlowDriver(grid=grid, options=pf_options)
        # pf_drv.run()

        opf_options = vge.OptimalPowerFlowOptions(
            solver=vge.SolverType.NONLINEAR_OPF,
            # ips_init_with_pf=pf_drv.results.converged,
            ips_init_with_pf=False,
            ips_tolerance=1e-5,
            ips_iterations=60,
            ips_trust_radius=1.0,
            ips_control_q_limits=True,
            # acopf_v0=pf_drv.results.voltage,
            # acopf_S0=pf_drv.results.Sbus,
            acopf_mode=vge.AcOpfMode.ACOPFslacks
        )

        t1 = datetime.now()
        opf_driver = vge.OptimalPowerFlowDriver(grid=grid, options=opf_options)
        opf_driver.run()
        opf_res = opf_driver.results
        dt = datetime.now() - t1

        data[name] = {
            'name': name,
            'n buses': grid.get_bus_number(),
            'n branches': grid.get_branch_number(),
            'n generators': grid.get_generators_number(),
            'Error': opf_res.error,
            'Converged': opf_res.converged,
            'time (s)': dt.seconds
        }

        print("-" * 80)
        print(name)
        # print(opf_res.get_bus_df())
        print("Error", opf_res.error)
        print("Converged:", opf_res.converged)
        print("-" * 80)

        if opf_res.converged:
            converged_count += 1

        total += 1

df = pd.DataFrame(data=data).transpose()
df.to_excel("ACOPF_benchmark.xlsx")
print(f"Converged {converged_count} of {total}")
