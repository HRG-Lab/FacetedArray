from context import facetedarray

import csv

import numpy as np

from facetedarray import helpers
from facetedarray.core import CircularArray, FacetedArray

mag_path = 'test_files/rE_Plot_mag_1_32.csv'
phase_path = 'test_files/rE_Plot_phase_1_32.csv'

magdBTheta = []
with open(mag_path) as f:
    next(f)
    csv_reader = csv.reader(f)
    for row in csv_reader:
        magdBTheta.append(float(row[3]))

phaseTheta = []
with open(phase_path) as f:
    next(f)
    csv_reader = csv.reader(f)
    for row in csv_reader:
        phaseTheta.append(float(row[3]))

def A(phi):
    phi = helpers.rad_to_deg(phi)
    phi = int(phi)
    phi = helpers.shift_to_plus_minus_180(phi)
    phi += 180
    mag = magdBTheta[int(phi)]
    phase = phaseTheta[int(phi)]

    mag = 10**(mag/10)
    phase = helpers.deg_to_rad(phase)

    value = mag*np.cos(phase) + 1j*mag*np.sin(phase)

    return value

array = FacetedArray(
    frequency = 28E9,
    num_elements = 32,
    num_facets = 32,
    array_angles = [],
    element_pattern = A
)

array.plot_magnitude(16)