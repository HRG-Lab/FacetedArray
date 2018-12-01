import csv
import numpy as np

pi = np.pi

def deg_to_rad(deg):
    return deg * (pi / 180)

def rad_to_deg(rad):
    return rad * (180 / pi)

def to_dB(mag):
    return 10 * np.log10(abs(mag))

def shift_to_plus_minus_180(ang):
    while ang < -180:
        ang += 360
    while ang > 180:
        ang -= 360
    return ang

def import_pattern_data_from_csv(path, dataIndex):
    """Imports a .csv file to an array of magnitude values

    Args:
        path: The path to the csv file
        dataIndex: The index of the data of interest. If it's the fourth column,
            this would be 3

    Returns:
        An array containing the imported data
    """

    array = []
    with open(path) as f:
        next(f) # This skips the first line
        csv_reader = csv.reader(f)
        for row in csv_reader:
            array.append(float(row[dataIndex]))

    return array
