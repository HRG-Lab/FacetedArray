import numpy as np
from .helpers import deg_to_rad,rad_to_deg,to_dB,shift_to_plus_minus_180,import_pattern_data_from_csv

pi = np.pi

def create_element_pattern_func_from_csv(
    magdBTheta_path,
    magdBTheta_index,
    phaseTheta_path,
    phaseTheta_index
):
    magdBTheta = import_pattern_data_from_csv(magdBTheta_path, magdBTheta_index)
    phaseTheta = import_pattern_data_from_csv(phaseTheta_path, phaseTheta_index)

    def A(phi):
        phi = rad_to_deg(phi)
        phi = int(phi)
        phi = shift_to_plus_minus_180(phi)
        phi += 180

        mag = magdBTheta[phi]
        mag = 10**(mag / 10)
        phase = phaseTheta[phi]
        phase = deg_to_rad(phase)

        value = (mag * np.cos(phase)) + (1j * mag * np.sin(phase))

        return value

    return A

def create_E_func(element_pattern, num_elements, radius, wavelen, current_mag=1):
    """ Creates a function which calculates the radiation pattern of a multimode array

    The E function is the implementation of equation (9) from Sheleg 1968
    "A Matrix-Fed Circular Array for Continuous Scanning"

    #TODO: should current mag be an array of magnitudes per element?
    Args:
        element_pattern: Function which represents the element pattern
        num_elements: Number of elements
        radius: The radius of the circular array
        wavelen: The wavelength of the radiating frequency
        current_mag: Magnitude of current on an element (default: 1)

    Returns:
        E: Function which represents the circular array pattern
    """
    alpha_j = lambda J: J * 2 * pi / num_elements
    psi_j = lambda J, mode_num: alpha_j(J) * mode_num

    def E(phi, mode_num):
        Ee = 0
        for J in range(1, num_elements + 1):
            Ee += (
                    current_mag *
                    np.exp(1j * psi_j(J, mode_num)) *
                    element_pattern(phi - alpha_j(J)) *
                    np.exp(1j * (2 * pi * radius / wavelen) * np.cos(phi - alpha_j(J)))
            )
        return Ee

    return E

def printshifts(E, smoothphase):
    """ Prints the...?

    Args:
        E: Function pointer for array pattern function created by 'create_E_func'
        smoothphase: Array of element phases for non-faceted (smooth) array
    """
    shiftarray = []

    print('Mode\tNewPhase\tIdeal Phase')

    for K in range(0,17):
        shiftarray.append(np.angle(E(0, K), True))

    init = shiftarray[0]
    for K in range(0, 17):
        shiftarray[K] = shiftarray[K] - init
        shiftarray[K] = shift_to_plus_minus_180(shiftarray[K])

        print(str(K) + '\t' +
              str(np.round(shiftarray[K], 2)) + '\t\t' +
              str(np.round(rad_to_deg(smoothphase[K]), 2)))

        shiftarray[K] = deg_to_rad(shiftarray[K])
