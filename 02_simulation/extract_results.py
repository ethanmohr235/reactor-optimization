import openmc
import json
from pathlib import Path
import time
import os

def extract(run_dir, metadata, outpath):
    cwd = os.getcwd()
    os.chdir(run_dir)
    
    sp = openmc.StatePoint("statepoint.20.h5")
    summary = {
        **metadata,
        "keff_mean": float(sp.keff.n),
        "keff_std": float(sp.keff.s),
    }

    with open(outpath, "w") as f:
        json.dump(summary, f, indent=2)
    
    os.chdir(cwd)
