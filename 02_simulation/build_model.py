# Imports
import openmc
import numpy as np

def build_model(config):
    # Get variables from the config file
    yml_geom = config["geometry"]
    yml_sett = config["settings"]

    # UO2, cladding, and water for basic testing
    uo2 = openmc.Material(name="UO2")
    uo2.set_density("g/cm3", 10.4)

    uo2.add_nuclide("U235", 1.0)
    uo2.add_nuclide("U238", 4.0)
    uo2.add_element("O", 10.0)

    water = openmc.Material(name="Water")
    water.set_density("g/cm3", 1.0)

    water.add_element("H", 2.0)
    water.add_element("O", 1.0)

    cladding = openmc.Material(name="Zirconium cladding")
    cladding.set_density("g/cm3", 6.55)

    cladding.add_element("Zr", 1.0)

    materials = openmc.Materials([uo2, water, cladding])

    # Define a simple pin cell geometry
    fuel_radius = yml_geom["fuel_radius"]
    clad_thickness = yml_geom["clad_thickness"]
    gap = yml_geom["gap"]
    pitch = yml_geom["pitch"]
    half_pitch = pitch / 2

    # Simplest possible volume for testing
    xmin = openmc.XPlane(x0=-half_pitch, boundary_type="reflective")
    xmax = openmc.XPlane(x0= half_pitch, boundary_type="reflective")
    ymin = openmc.YPlane(y0=-half_pitch, boundary_type="reflective")
    ymax = openmc.YPlane(y0= half_pitch, boundary_type="reflective")

    fuel_surf = openmc.ZCylinder(r=fuel_radius)
    clad_inner_surf = openmc.ZCylinder(r=fuel_radius + gap)
    clad_outer_surf = openmc.ZCylinder(r=fuel_radius + gap + clad_thickness)

    fuel_region = (
        -fuel_surf
        & +xmin & -xmax
        & +ymin & -ymax
    )

    clad_region = (
        +fuel_surf
        & -clad_outer_surf
        & +xmin & -xmax
        & +ymin & -ymax
    )

    water_region = (
        +clad_outer_surf
        & +xmin & -xmax
        & +ymin & -ymax
    )

    fuel_cell = openmc.Cell(name="fuel_cell", fill=uo2, region=fuel_region)
    clad_cell = openmc.Cell(name="clad_cell", fill=cladding, region=clad_region)
    water_cell = openmc.Cell(name="water_cell", fill=water, region=water_region)

    geometry = openmc.Geometry([fuel_cell, clad_cell, water_cell])

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

    # Tallies for flux and fission in the water and fuel
    energy_bins = np.logspace(-5, 7, 200)  # eV
    energy_filter = openmc.EnergyFilter(energy_bins)

    fuel_filter = openmc.CellFilter(fuel_cell)
    water_filter = openmc.CellFilter(water_cell)

    fuel_flux = openmc.Tally(name="fuel_flux_spectrum")
    fuel_flux.filters = [fuel_filter, energy_filter]
    fuel_flux.scores = ["flux"]

    water_flux = openmc.Tally(name="water_flux_spectrum")
    water_flux.filters = [water_filter, energy_filter]
    water_flux.scores = ["flux"]

    fission_spectrum = openmc.Tally(name="fission_energy")
    fission_spectrum.filters = [fuel_filter, energy_filter]
    fission_spectrum.scores = ["fission"]

    tallies = openmc.Tallies([
        fuel_flux,
        water_flux,
        fission_spectrum
    ])
    
    model.tallies = tallies

    # Ship it out to run.py
    return model