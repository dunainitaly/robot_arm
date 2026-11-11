"""
Point-Plane Projection
======================

Project a point onto a plane.

"""
import matplotlib.pyplot as plt
from skspatial.objects import Plane, Points
from skspatial.plotting import plot_3d

plane = Plane(point=[0, 0, 2], normal=[1, 0, 2])

points = Points([
    [5, 9, 2],
    [5, 9, 3],
    [3, 5, 7],
])

points_projected = plane.project_points(points)

fig, ax = plot_3d(
    plane.plotter(lims_x=(0, 10), lims_y=(0, 15), alpha=0.3),
    points.plotter(s=75, c='k'),
    points_projected.plotter(c='r', s=75, zorder=3),
)

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

plt.show()


from skspatial.objects import Plane, Point, Vector

plane = Plane(point=[0, 0, 2], normal=[1, 0, 2])
point = Point([5, 9, 3])

point_projected = plane.project_point(point)
print(point_projected)
