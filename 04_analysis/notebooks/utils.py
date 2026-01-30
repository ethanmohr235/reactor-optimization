# Helper functions for all analysis notebooks
def find_statepoint(run_dir):
    files = list(run_dir.glob("statepoint.*.h5"))
    assert len(files) == 1
    return files[0]
