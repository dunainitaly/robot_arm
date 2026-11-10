import numpy as np
from svgpathtools import svg2paths


def svg_to_points(filename, spacing=2, offset=(0, 0)):
    paths, attributes = svg2paths(filename)

    points = []
    offset = offset[0] + offset[1] * 1j

    for path in paths:
        length = path.length()

        if length == 0:
            continue

        distances = np.arange(0, length, spacing)

        for distance in distances:
            t = path.ilength(distance)
            pos = path.point(t) + offset

            points.append([pos.real, pos.imag, 0.0])

    return points
