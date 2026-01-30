import openmc
import json
from pathlib import Path
import time
import os

def extract(run_dir, metadata, outpath):

    # Go to the results folder
    cwd = os.getcwd()
    os.chdir(run_dir)
    
    # Make some metadata to add to the .json file
    sp = openmc.StatePoint("statepoint.20.h5")
    summary = {
        **metadata,
        "keff_mean": float(sp.keff.n),
        "keff_std": float(sp.keff.s),
    }

    # Create teat .json file in the results folder
    with open(outpath, "w") as f:
        json.dump(summary, f, indent=2)

    # Return to original directory
    os.chdir(cwd)
