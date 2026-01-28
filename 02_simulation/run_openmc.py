import openmc
import os

def run_openmc(model, run_dir):
    cwd = os.getcwd()
    os.chdir(run_dir)

    model.export_to_xml()
    openmc.run(output=False)
    print(f'SIMULATION COMPLETED')
    
    os.chdir(cwd)
    