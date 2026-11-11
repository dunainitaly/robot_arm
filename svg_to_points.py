import numpy as np
from svgpathtools import svg2paths

Point = tuple[float, float, float]
Line = list[Point]

def svg_to_points(filename: str, spacing: int = 2, offset: Point = (0, 0, 0)) -> list[Line]:
    '''
    converts svg lines to list of points through which the line goes

    filename: str     svg file path
    spacing: int      
    offset: tuple[float, float, float]

    returns list of lines, where each line is list of points (tuple[float,float,float])
    '''

    paths, attributes = svg2paths(filename)
    points: list[Line] = []
    offset_calc = offset[0] + offset[1] * 1j

    for path in paths:
        line: Line = []
        length = path.length()

        if length == 0:
            continue

        distances = np.arange(0, length, spacing)

        for distance in distances:
            t = path.ilength(distance)
            pos = path.point(t) + offset_calc

            line.append((pos.real, pos.imag, offset[2]))
        points.append(line)
    return points


if __name__ == "__main__":
    svg_to_points("test.svg",spacing=4, offset=(20,100, 2))
