# Imports
import openmc

def build_model(config):
    # Simplest possible material for testing
    fuel = openmc.Material(name="fuel")
    fuel.set_density("g/cm3", 10.0)

    fuel.add_nuclide("U235", 1.0)
    fuel.add_nuclide("U238", 4.0)

    materials = openmc.Materials([fuel])

    # Simplest possible volume for testing
    xmin = openmc.XPlane(x0=-50.0, boundary_type="reflective")
    xmax = openmc.XPlane(x0= 50.0, boundary_type="reflective")
    ymin = openmc.YPlane(y0=-50.0, boundary_type="reflective")
    ymax = openmc.YPlane(y0= 50.0, boundary_type="reflective")
    zmin = openmc.ZPlane(z0=-50.0, boundary_type="reflective")
    zmax = openmc.ZPlane(z0= 50.0, boundary_type="reflective")

    region = +xmin & -xmax & +ymin & -ymax & +zmin & -zmax

    cell = openmc.Cell(name="infinite_medium", fill=fuel, region=region)
    geometry = openmc.Geometry([cell])

    # Eigenvalue mode and simulation settings
    settings = openmc.Settings()
    settings.run_mode = "eigenvalue"

    settings.particles = 1000
    settings.batches = 20
    settings.inactive = 5

    settings.seed = 12345

    # Combine into one model
    model = openmc.Model(
        materials=materials,
        geometry=geometry,
        settings=settings
    )

    # Add simplest possible tally for testing
    tally = openmc.Tally(name="flux")
    tally.filters = [openmc.CellFilter(cell)]
    tally.scores = ["flux"]

    tallies = openmc.Tallies([tally])
    model.tallies = tallies

    # Ship it out to run.py
    return model