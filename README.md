FacetedArray
============

The goal of this package is to generalize Karl's faceted array code and provide
a nice interface.

## How to use
This code is primarily organized around two classes: `CircularArray` and `FacetedArray` which inherits from `CircularArray`. To use either, you define a function which represents your element pattern and create an object:

```python
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
```

More detailed examples are provided in the `tests` directory. If you are working with a configuration that has more than one element per facet, you need to define your element pattern function such that it takes and index of which element on the facet you're on. For example:

```python
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
```

## Important
When you are working with a configuration that has more than one element per facet, you must specify the angle where the center of the element is located (in radians). For example:

```python
array = FacetedArray(
    frequency = 28E9,
    num_elements = 32,
    num_facets = 16,
    array_angles = [0.09342412368, np.pi/8 - 0.09342412368], # <-- Passed here as a list
    element_pattern = A
)
```