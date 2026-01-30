# Imports
import shutil
from pathlib import Path
import yaml
import copy
from datetime import datetime

from build_model import build_model
from run_openmc import run_openmc
from extract_results import extract

import openmc

# Main function -- hooked to other scripts in folder
def main():

    # Where is the config file?
    config_path = Path("configs/ex_01_moderation_fraction.yml")

    # Open the config file and load it
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    # Get the variable to iterate on successive simulations
    geom = config["geometry"]
    sweep_vars = {
        k: v for k, v in geom.items()
        if isinstance(v, list)
    }

    if len(sweep_vars) == 0:
        print("One-off config file")
        run_simulation(config)

    elif len(sweep_vars) > 1:
        raise ValueError("Only one sweep variable allowed per run")

    else:
        sweep_var, values = next(iter(sweep_vars.items()))
        print(f"Sweeping {sweep_var} over {values}")

        for val in values:
            this_config = copy.deepcopy(config)
            this_config["geometry"][sweep_var] = val
            print(f"Running simulation with {sweep_var} = {val}")
            run_simulation(this_config)

def run_simulation(config):
    # Get the time and make a new folder for results from this run
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = Path("runs") / f"run_{timestamp}"
    run_dir.mkdir(parents=True)

    # Drop the config file in the results folder
    with open(run_dir / "config_used.yml", "w") as f:
        yaml.safe_dump(config, f, sort_keys=False)

    # Build and run the model
    model = build_model(config)
    run_openmc(model, run_dir)

    # Log some more data

    extract(
        run_dir, 
        make_metadata(config), 
        "summary.json"
    )

def make_metadata(config):
    metadata = {
        # sweep variable
        "fuel_radius": config["geometry"]["fuel_radius"],

        # derived geometry
        "clad_thickness" : config["geometry"]["clad_thickness"],
        "pitch": config["geometry"]["pitch"],

        # Monte Carlo
        "particles": config["settings"]["particles"],
        "batches": config["settings"]["batches"],
        "inactive": config["settings"]["inactive"],

        # provenance
        "openmc_version": openmc.__version__,
    }

    return metadata

if __name__ == "__main__":
    main()