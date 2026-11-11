import numpy as np
from svgpathtools import svg2paths


def svg_to_points(filename, spacing=2, offset: tuple[float, float, float] = (0, 0, 0)) -> list[tuple[float, float, float]]:
    '''
    converts svg lines to list of points through which the line goes

    filename: str     svg file path
    spacing: int      
    offset: tuple[float, float, float]
    '''

    paths, attributes = svg2paths(filename)

    points: list[tuple[float, float, float]] = []
    offset_calc = offset[0] + offset[1] * 1j

    # will not work for multiple lines if they aren't connected !!!
    for path in paths:
        length = path.length()

        if length == 0:
            continue

        distances = np.arange(0, length, spacing)

        for distance in distances:
            t = path.ilength(distance)
            pos = path.point(t) + offset_calc

            points.append((pos.real, pos.imag, offset[2]))

    return points
