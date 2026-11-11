import numpy as np
from ikpy.utils import geometry
from robot import robot
import matplotlib.pyplot as plt
from typing import List, Dict
import svg_to_points as svg
import matplotlib.pyplot as plt
from skspatial.objects import Plane, Point, Vector, Points
from skspatial.plotting import plot_3d


# start joint configuration
current_joints = np.zeros(len(robot.links))
np.set_printoptions(precision=2, suppress=True)

def project_to_plane(plane: Plane, points: Points) -> list[list[float]]:
    return np.asarray(plane.project_points(points))

def points_to_frames(points: list, orientation_matrix: np.ndarray):
    frames = []

    for point in points:
        matrix = np.eye(4)
        matrix[:3, :3] = orientation_matrix
        matrix[:3, 3] = point
        frames.append(matrix)

    return frames

def visualise(points):
    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111, projection="3d")
    for i in range (10):
        # iterr = 0
        for angles in trajectory:
            ax.clear()
            robot.plot(angles, ax, target=list(points[-1]))
            ax.scatter(
                points[:, 0],
                points[:, 1],
                points[:, 2],
                c='red',
                s=10,
                label="Projected points"
            )
            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            ax.set_zlabel("Z")
            ax.set_xlim(-100, 200)
            ax.set_ylim(-100, 200)
            ax.set_zlim(0, 300)
            # fig.savefig(f'./images/out{iterr}', bbox_inches='tight', pad_inches=0)
            plt.pause(0.025)
            # iterr+=1
    plt.show()

points = svg.svg_to_points("test.svg", spacing=4, offset=(0, -100))



plane = Plane(point=[0, 0, 0], normal=[0, 0, 1])
points = project_to_plane(
    plane=plane,
    points=Points(points)
)

frames = points_to_frames(points, np.array([
    [ 0, 0,  1],
    [ 0, 1,  0],
    [-1, 0,  0],
]))
print(frames)
points =  np.asarray(points)
trajectory = robot.inverse_kinematics_trajectory_frame(
    frames,
    initial_position=current_joints,
    orientation_mode="all",
    regularization_parameter=0.01
)
# print(trajectory)


for frame, joints in zip(frames, trajectory):
    print(robot.forward_kinematics(joints))


visualise(points)



#| Axis    | Color  | Code                 |
#| ------- | ------ | -------------------- |
#| Local X | Green  | directions_colors[0] |
#| Local Y | Cyan   | directions_colors[1] |
#| Local Z | Orange | directions_colors[2] |
