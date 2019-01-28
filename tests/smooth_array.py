from context import facetedarray

import csv

import numpy as np

from facetedarray import helpers
from facetedarray.core import CircularArray, FacetedArray

mag_path = 'test_files/rE_Plot_mag.csv'
phase_path = 'test_files/rE_Plot_phase.csv'

magdBThetaS = []
with open(mag_path) as f:
    next(f)
    csv_reader = csv.reader(f)
    for row in csv_reader:
        magdBThetaS.append(float(row[1]))

phaseThetaS = []
with open(phase_path) as f:
    next(f)
    csv_reader = csv.reader(f)
    for row in csv_reader:
        phaseThetaS.append(float(row[3]))

def A(phi):
    phi = helpers.rad_to_deg(phi)
    phi = np.round(phi, 0)
    phi = helpers.shift_to_plus_minus_180(phi)
    phi += 180

    mag = magdBThetaS[int(phi)]
    mag = 10**(mag / 10)
    phase = phaseThetaS[int(phi)]
    phase = helpers.deg_to_rad(phase)

    value = mag * np.cos(phase) + 1j * mag * np.sin(phase)

    return value


array = CircularArray(
    frequency = 28E9,
    num_elements = 32,
    element_pattern = A
)

array.plot_magnitude(16)
