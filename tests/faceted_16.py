from context import facetedarray

import csv

import numpy as np

from facetedarray import helpers
from facetedarray.core import CircularArray, FacetedArray

mag1_path = 'test_files/rE_Plot_mag_1_16.csv'
mag2_path = 'test_files/rE_Plot_mag_2_16.csv'
phase1_path = 'test_files/rE_Plot_phase_1_16.csv'
phase2_path = 'test_files/rE_Plot_phase_2_16.csv'

magdBTheta1 = []
with open(mag1_path) as f:
    next(f)
    csv_reader = csv.reader(f)
    for row in csv_reader:
        magdBTheta1.append(float(row[4]))

magdBTheta2 = []
with open(mag2_path) as f:
    next(f)
    csv_reader = csv.reader(f)
    for row in csv_reader:
        magdBTheta2.append(float(row[4]))

phaseTheta1 = []
with open(phase1_path) as f:
    next(f)
    csv_reader = csv.reader(f)
    for row in csv_reader:
        phaseTheta1.append(float(row[4]))

phaseTheta2 = []
with open(phase2_path) as f:
    next(f)
    csv_reader = csv.reader(f)
    for row in csv_reader:
        phaseTheta2.append(float(row[4]))

def A(phi, element):
    phi = helpers.rad_to_deg(phi)
    phi = int(phi)
    phi = helpers.shift_to_plus_minus_180(phi)
    phi += 180
    if element == 1:
        mag = magdBTheta1[int(phi)]
        phase = phaseTheta1[int(phi)]
    else:
        mag = magdBTheta2[int(phi)]
        phase = phaseTheta2[int(phi)]

    mag = 10**(mag/10)
    phase = helpers.deg_to_rad(phase)

    value = mag*np.cos(phase) + 1j*mag*np.sin(phase)

    return value

array = FacetedArray(
    frequency = 28E9,
    num_elements = 32,
    num_facets = 16,
    array_angles = [0.09342412368, np.pi/8 - 0.09342412368],
    element_pattern = A
)

array.plot_magnitude(16)