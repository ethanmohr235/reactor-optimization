import openmc
import os

def run_openmc(model, run_dir):
    os.chdir(run_dir)
    model.export_to_xml()
    openmc.run()
