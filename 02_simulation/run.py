# Imports
from pathlib import Path
import yaml
from datetime import datetime
from build_model import build_model
from run_openmc import run_openmc

# Main function -- hooked to other scripts in folder
def main():
    # Where is the config file?
    config_path = Path("configs/baseline.yml")

    # Open the config file and load it
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    # Get the time and make a new folder for results from this run
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = Path("runs") / f"run_{timestamp}"
    run_dir.mkdir(parents=True)

    # Build and run the model
    model = build_model(config)
    run_openmc(model, run_dir)

if __name__ == "__main__":
    main()