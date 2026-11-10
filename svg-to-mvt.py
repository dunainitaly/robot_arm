import numpy as np
from ikpy.utils import geometry
from robot import robot
import matplotlib.pyplot as plt
from typing import List, Dict
import svg_to_points as svg

# start joint configuration
current_joints = np.zeros(len(robot.links))
np.set_printoptions(precision=2)


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
        for angles in trajectory:
            ax.clear()
            robot.plot(angles, ax, target=list(points[-1]))

            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            ax.set_zlabel("Z")
            ax.set_xlim(-200, 200)
            ax.set_ylim(-200, 200)
            ax.set_zlim(0, 300)

            plt.pause(0.025)

    plt.show()

points = svg.svg_to_points(100, "test.svg")
frames = points_to_frames(points, np.array([
    [1,  0,  0],
    [0, -1,  0],
    [0,  0, -1]
]))

trajectory = robot.inverse_kinematics_trajectory_frame(
    frames,
    initial_position=current_joints,
    orientation_mode="Y",
    regularization_parameter=0.01
)

visualise(points)


#| Axis    | Color  | Code                 |
#| ------- | ------ | -------------------- |
#| Local X | Green  | directions_colors[0] |
#| Local Y | Cyan   | directions_colors[1] |
#| Local Z | Orange | directions_colors[2] |
