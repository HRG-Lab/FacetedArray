import math
import cmath
import matplotlib.pyplot as plt
import numpy as np
import csv

from collections import deque

from emplots import rectangular

from context import facetedarray
from facetedarray.helpers import deg_to_rad, to_dB
from facetedarray.core import print_phaseshifts, phaseshifts, create_E_func, create_sum_E_func, create_element_pattern_func_from_csv

# TODO: Where is this from?
smoothphase = [0, -4.69984,5.00602,12.364967,19.43257,44.21539,51.1145,81.16565,107.8338,134.1925,169.2242,-140.6595,-114.2837,-58.93227,-11.99662,101.49356,136.80026]
smoothphase = [deg_to_rad(smoothphase[i]) for i in range(len(smoothphase))]

pi = np.pi
C = 3E8
F = 28E9
N = 32
wavelen = 6.6E-3
radius = wavelen * N / (4 * pi)

A = create_element_pattern_func_from_csv('test_files/rE_Plot_mag_1_32.csv', 3,
    'test_files/rE_Plot_phase_1_32.csv', 3)

E = create_E_func(element_pattern=A, num_elements=32, radius=radius, wavelen=wavelen)

shiftarray = phaseshifts(E, smoothphase)
sumE = create_sum_E_func(element_pattern=A, num_elements=32, radius=radius, wavelen=wavelen, phaseshifts=shiftarray)
smoothE = create_sum_E_func(element_pattern=A, num_elements=32, radius=radius, wavelen=wavelen, phaseshifts=smoothphase)

phis = np.arange(0, 2*pi, pi / 180)
mags = [sumE(phi, 16) for phi in phis]
smooth_mags = [smoothE(phi, 16) for phi in phis]

# The center value isn't at phi = 0. This rotates the magnitude array
# such that the plot is centered at 0
mags = deque(mags)
mags.rotate(len(mags) // 2)
smooth_mags = deque(smooth_mags)
smooth_mags.rotate(len(smooth_mags) // 2)

rectangular.plot(angles=phis, magnitudes=smooth_mags, label="Smooth Phase")
rectangular.plot(angles=phis, magnitudes=mags, label="Faceted Phase")
plt.tight_layout()
plt.legend()
plt.show()
