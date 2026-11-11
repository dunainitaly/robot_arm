import numpy as np
from ikpy.utils import geometry
from robot import robot
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import List, Dict
import svg_to_points as svg
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

def visualise(points, trajectory):
    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111, projection="3d")

    def update(angles):
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

    def on_press(event):
        plt.close(fig)

    fig.canvas.mpl_connect("key_press_event", on_press)
    animation = FuncAnimation(
        fig,
        update,
        frames=trajectory,
        interval=25,
        repeat=True
    )
    plt.show()

if __name__ == "__main__":
    origin = (0, -100, 100)
    lines = svg.svg_to_points("C:\\Users\\misae\\Downloads\\logo_gml.cz.svg", spacing=4, offset=origin)
    for points in lines:
        plane = Plane(point=origin, normal=[0, 0, 1])
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


        visualise(points, trajectory)



    #| Axis    | Color  | Code                 |
    #| ------- | ------ | -------------------- |
    #| Local X | Green  | directions_colors[0] |
    #| Local Y | Cyan   | directions_colors[1] |
    #| Local Z | Orange | directions_colors[2] |
