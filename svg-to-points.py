
# Source - https://stackoverflow.com/a/69314131
# Posted by Riccardo Bucco
# Retrieved 2026-11-09, License - CC BY-SA 4.0


from pathlib import Path
import numpy as np
import svg.path
import re


def svg_to_points(n: int, filepath: str) -> list[list[float]]:
    content = Path(filepath).read_text()
    match = re.search(r'<path[^>]*\sd="([^"]+)"', content)

    if not match:
        raise ValueError("No SVG path found in file")

    pp = svg.path.parse_path(match.group(1))

    return [
        [float(p.real), float(p.imag), 0.0]
        for p in map(pp.point, np.linspace(0, 1, n))
    ]


if __name__ == "__main__":
    points = svg_to_points(10, "test.svg")
    print(points)
