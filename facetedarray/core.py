import numpy as np
from emplots import rectangular, polar
import matplotlib.pyplot as plt
from collections import deque

from . import helpers

pi = np.pi

class CircularArray:
    def __init__(self, *, frequency, num_elements, element_pattern):
        self.frequency = frequency
        self.num_elements = num_elements
        self.element_pattern = element_pattern
        self.radius_over_wavelen = self.num_elements / (4 * pi)

    def smooth_phase_corrections(self):
        # TODO: Is this correct?
        corrections = []
        for mode in range(0, self.num_elements // 2 + 1):
            corrections.append(np.angle(self.modal_contribution(0, mode), True))

        corrections = [phase - corrections[0] for phase in corrections]
        corrections = [helpers.shift_to_plus_minus_180(phase) for phase in corrections]
        corrections = [helpers.deg_to_rad(correction) for correction in corrections]
        
        return corrections

    def modal_contribution(self, phi, mode):
        phi_radians = helpers.deg_to_rad(phi)
        E = 0
        for elem in range(1, self.num_elements + 1):
            element_angle = elem * 2 * pi / self.num_elements
            element_current = 1 # TODO: Should this be adjustable?
            current_phase = 2 * pi * mode * elem / self.num_elements
            pattern = self.element_pattern(phi_radians - element_angle)
            phase = 2 * pi * self.radius_over_wavelen * np.cos(phi_radians - element_angle)

            E += (
                element_current *
                np.exp(1j * current_phase) *
                pattern *
                np.exp(1j * phase)
            )
        
        return E

    def array_pattern_with_phase_correction(self, phi, modes):
        Esum = 0
        phase_corrections = self.smooth_phase_corrections()
        for elem in range(1, self.num_elements + 1):
            Ksum = 0
            for mode in range(0, modes + 1):
                # TODO: This should be a parameter so you can test various 
                # tapers on the inputs to the Butler Matrix
                input_current = np.cos(mode * pi / 32) 
                input_phase = -1j * phase_corrections[mode]
                element_phase = elem * mode * 2 * pi / self.num_elements
                Ksum += input_current * np.exp(input_phase) * np.exp(1j * element_phase)
                # This accounts for modal symetry
                if (mode > 0 and mode < self.num_elements // 2):
                    Ksum += input_current * np.exp(input_phase) * np.exp(-1j * element_phase)
            element_angle = elem * 2 * pi / self.num_elements
            element_pattern = self.element_pattern(phi - element_angle)
            Esum += (
                Ksum * 
                element_pattern *
                np.exp(1j * 2 * pi * self.radius_over_wavelen * np.cos(phi - element_angle))
            )
        return Esum

    def plot_magnitude(self, modes):
        phis = np.arange(0, 2 * pi, pi / 180)
        mags = [self.array_pattern_with_phase_correction(phi, modes) for phi in phis]
        mags = deque(mags)
        mags.rotate(len(mags) // 2)
        rectangular.plot(angles=phis, magnitudes=mags, label="Circular Array")
        plt.tight_layout()
        plt.legend()
        plt.show()


class FacetedArray(CircularArray):
    def __init__(self, *, frequency, num_elements, num_facets, array_angles=[], element_pattern):
        CircularArray.__init__(
            self,
            frequency=frequency,
            num_elements=num_elements, 
            element_pattern=element_pattern
        )
        self.num_facets=num_facets
        self.array_angles = array_angles
        self.elements_per_facet = self.num_elements // self.num_facets
        self.total_facet_angle = 2 * pi / self.num_facets

    def faceted_angle(self, element, current_facet):
        start = -pi / self.num_facets + current_facet * self.total_facet_angle

        if self.num_elements == self.num_facets:
            angle = start + (pi / self.num_elements)
        else:
            angle = start + self.array_angles[element - 1]

        return angle


    def phase_corrections(self):
        # TODO: Is this correct?
        corrections = []
        for mode in range(0, self.num_elements // 2 + 1):
            corrections.append(np.angle(self.modal_contribution(0, mode), True))

        corrections = [phase - corrections[0] for phase in corrections]
        corrections = [helpers.shift_to_plus_minus_180(phase) for phase in corrections]
        corrections = [helpers.deg_to_rad(correction) for correction in corrections]
        
        return corrections

    def modal_contribution(self, phi, mode):
        facet = lambda J: (J + 1) // self.elements_per_facet 
        subelement = lambda J: J - facet(J) * self.elements_per_facet + self.elements_per_facet // 2

        phi_radians = helpers.deg_to_rad(phi)
        E = 0
        
        for elem in range(1, self.num_elements + 1):
            element_current = 1 # TODO: adjustable?
            current_facet = facet(elem)
            if elem > (self.num_elements - (self.elements_per_facet // 2)):
                current_facet = 0
            element_angle = self.faceted_angle(subelement(elem), current_facet) # TODO: Fix names
            if self.num_facets == self.num_elements:
                element_pattern = self.element_pattern(phi_radians - element_angle)
            else:
                element_pattern = self.element_pattern(phi_radians - element_angle, subelement(elem)) # TODO: Fix names
            current_phase = element_angle * mode
            E += (
                element_current *
                np.exp(1j * current_phase) * 
                element_pattern * 
                np.exp(1j * 2 * pi * self.radius_over_wavelen * np.cos(phi_radians - element_angle))
            )
        return E


    def array_pattern_with_phase_correction(self, phi, modes):
        Esum = 0
        phase_corrections = self.phase_corrections()
        facet = lambda J: (J + 1) // self.elements_per_facet 
        subelement = lambda J: J - facet(J) * self.elements_per_facet + self.elements_per_facet // 2
        for elem in range(1,self.num_elements + 1):
            Ksum = 0
            current_facet = facet(elem)
            element = subelement(elem)

            if elem > (self.num_elements - (self.elements_per_facet // 2)):
                current_facet = 0

            element_angle = self.faceted_angle(element, current_facet)

            for mode in range(0,modes + 1):
                input_current = np.cos(mode * pi/32)
                current_phase = element_angle * mode
                Ksum += (
                    input_current *
                    np.exp(-1j * phase_corrections[mode]) *
                    np.exp(1j * current_phase)
                )
                if (mode > 0 and mode < (self.num_elements // 2)):
                    Ksum += (
                        input_current *
                        np.exp(-1j * phase_corrections[mode]) *
                        np.exp(-1j * current_phase)
                    )

            if self.num_facets == self.num_elements:
                element_pattern = self.element_pattern(phi - element_angle)
            else:
                element_pattern = self.element_pattern(phi - element_angle, subelement(elem)) # TODO: Fix names
            Esum += (
                Ksum * 
                element_pattern *
                np.exp(1j * 2 * pi * self.radius_over_wavelen * np.cos(phi - element_angle))
            )
        return Esum

    def plot_magnitude(self, modes):
        phis = np.arange(0, 2 * pi, pi / 180)
        mags = [self.array_pattern_with_phase_correction(phi, modes) for phi in phis]
        mags = deque(mags)
        mags.rotate(len(mags) // 2)
        rectangular.plot(angles=phis, magnitudes=mags, label="Circular Array")
        plt.tight_layout()
        plt.legend()
        plt.show()