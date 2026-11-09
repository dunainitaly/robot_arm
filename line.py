import numpy as np
from ikpy.utils import geometry
from robot import robot
import matplotlib.pyplot as plt
from typing import List, Dict


# start joint configuration
current_joints = np.zeros(len(robot.links))
np.set_printoptions(precision=2)
def interpolate_points(
    endpoints: list[list[float, float, float], list[float, float, float]],
    n: int = 10,
    endpoint: bool = True,
) -> np.ndarray:
    """Return n points evenly spaced along the segment between two 3D positions."""
    a, b = np.asarray(endpoints, dtype=float)
    t = np.linspace(0.0, 1.0, n, endpoint=endpoint)[:, None]
    return a + t * (b - a)

def points_to_frames(points:List[float,float,float],orientation_matrix):
    frames = []
    for point in points:
        matrix = np.eye(4)
        matrix[:-1, :-1] = orientation_matrix
        matrix[:-1, -1] = point 
        frames.append(matrix)
    return frames

def visualise():
    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111, projection="3d")
    for i in range (10):
        for angles in trajectory:
            ax.clear()
            robot.plot(angles, ax, target=list(end))

            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            ax.set_zlabel("Z")
            ax.set_xlim(-200, 200)
            ax.set_ylim(-200, 200)
            ax.set_zlim(0, 300)

            plt.pause(0.025)

    plt.show()


#start = geometry.to_transformation_matrix([120, 10, 10], np.eye(3))
#end = geometry.to_transformation_matrix([100, 50, 10], geometry.rz_matrix(np.pi))
#end = geometry.to_transformation_matrix([150, 175, 10], geometry.ry_matrix(np.pi))
start = geometry.to_transformation_matrix([0, 170, 0], np.eye(3)) 
end =  geometry.to_transformation_matrix([170, 0, 0], np.eye(3))

frames = geometry.interpolate_frames(start, end, 30)

frames = points_to_frames(interpolate_points([[0, 170, 0],[170,0,0]]), np.eye(3))
trajectory = robot.inverse_kinematics_trajectory_frame(
    frames,
    initial_position=current_joints,
    orientation_mode=None,
    regularization_parameter=0.01
)

# points_to_frames([[0, 170, 0],[170,0,0]], np.eye(3))
visualise()


#| Axis    | Color  | Code                 |
#| ------- | ------ | -------------------- |
#| Local X | Green  | directions_colors[0] |
#| Local Y | Cyan   | directions_colors[1] |
#| Local Z | Orange | directions_colors[2] |
