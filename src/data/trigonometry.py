import numpy


# Functions for calculating side lengths
class Pythagoras:
    @staticmethod
    # Returns the base for two given right-angle triangle lengths
    def get_base(a: float, c: float):
        return numpy.sqrt(c**2 - a**2)


# Returns triangle height for a given area and base
def get_height(area: float, base: float) -> float:
    return 2 * (area / base)


# Returns the triangle area for given side lengths
def get_area(a: float, b: float, c: float) -> float:
    return 0.25 * numpy.sqrt((a + b + c) * (-a + b + c) * (a - b + c) * (a + b - c))


# Returns an xy value relative to the leftmost corner
def get_reference(base: int, l1: float, l2: float) -> tuple:
    area = get_area(l1, l2, base)

    y = get_height(area, base)
    x = Pythagoras.get_base(y, l1)

    return (x, y)
