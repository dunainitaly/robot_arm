import numpy as np
from ikpy.utils import geometry
from robot import robot
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import List, Dict
import svg_to_points as svg
from skspatial.objects import Plane, Point, Vector, Points
from skspatial.plotting import plot_3d
from points_to_mvt_line import linear_move
from mvt_to_winsos import angles_to_sos


# start joint configuration
current_joints = np.zeros(len(robot.links))
np.set_printoptions(precision=2, suppress=True)

def interpolate_points(
    endpoints: tuple[tuple[float, float, float],tuple[float, float, float]],
    n: int = 10,
    endpoint: bool = True,
) -> np.ndarray:
    """Return n points evenly spaced along the segment between two 3D positions."""
    a, b = np.asarray(endpoints, dtype=float)
    t = np.linspace(0.0, 1.0, n, endpoint=endpoint)[:, None]
    return a + t * (b - a)

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

def move(start_point: tuple[float, float, float], end_point: tuple[float, float, float]):
    _, trajectory = linear_move(start_point, end_point)
    return trajectory

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
    origin = (10, 10, -70)
    plane = Plane(point=origin, normal=[0, 0, 1])

    travel_height = 10

    lines = svg.svg_to_points("drawing.svg", spacing=4, offset=origin)
    points_unpacked = []
    complete_trajectory = []
    for line in lines:
        for point in line:
            points_unpacked.append(point)
    
    all_points = project_to_plane(
                plane=plane,
                points=Points(points_unpacked)
            )
    print(lines)

    previous_path_end = None
    pen_orientation = np.array(np.eye(3))    
    all_frames = []
    travel_frames = []

    for points in lines:

        points = project_to_plane(
            plane=plane,
            points=Points(points)
        )

        drawing_frames = points_to_frames(points, pen_orientation)

        if previous_path_end is not None:
            travel_start, travel_end = project_to_plane(plane = travel_plane, points=Points([previous_path_end,drawing_frames[0][:3, -1]]))
            travel_points = interpolate_points((travel_start,travel_end))
            travel_frames = points_to_frames(travel_points, pen_orientation)

        points =  np.asarray(points)

        #for frame, joints in zip(frames, trajectory):
            #print(robot.forward_kinematics(joints))
        
        previous_path_end=drawing_frames[-1][:3, -1]
        all_frames.extend(travel_frames)
        all_frames.extend(drawing_frames)


    trajectory = robot.inverse_kinematics_trajectory_frame(
        all_frames,
        initial_position=current_joints,
        orientation_mode="all",
        regularization_parameter=0.001
    )
    visualise(all_points, trajectory)
    angles_to_sos(trajectory)


