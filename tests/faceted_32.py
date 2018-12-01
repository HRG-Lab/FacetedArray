import math
import cmath
import matplotlib.pyplot as plt
import numpy as np
import csv

from context import facetedarray
from facetedarray.helpers import deg_to_rad
from facetedarray.core import printshifts, create_E_func, create_element_pattern_func_from_csv

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

E = create_E_func(A, 32, radius, wavelen)

printshifts(E, smoothphase)
