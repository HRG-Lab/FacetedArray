from context import facetedarray

import pytest
import numpy as np

from facetedarray import helpers

def test_deg_to_rad():
    assert helpers.deg_to_rad(45) == np.pi / 4

def test_rad_to_deg():
    assert helpers.rad_to_deg(np.pi/4) == 45

def test_to_dB():
    assert helpers.to_dB(0.1) == -10

def test_shift_to_plus_minus_180():
    assert helpers.shift_to_plus_minus_180(180) == 180
    assert helpers.shift_to_plus_minus_180(-180) == -180
    assert helpers.shift_to_plus_minus_180(540) == 180
    assert helpers.shift_to_plus_minus_180(-540) == -180
    assert helpers.shift_to_plus_minus_180(360) == 0
    assert helpers.shift_to_plus_minus_180(-360) == 0