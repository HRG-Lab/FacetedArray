import numpy as np

pi = np.pi

def deg_to_rad(degrees):
    return degrees * pi / 180

def rad_to_deg(radians):
    return radians * 180 / pi

def to_dB(magnitude):
    return 10 * np.log10(abs(magnitude))

def shift_to_plus_minus_180(angle):
    while angle < -180:
        angle += 360
    while angle > 180:
        angle -= 360
    return angle