import numpy as np
from ikpy.utils import geometry
from robot import robot
import matplotlib.pyplot as plt

# Current joint configuration: one value per link, including fixed links.
current_joints = np.zeros(len(robot.links))
np.set_printoptions(precision=2)

start = geometry.to_transformation_matrix([200, 10, 10], np.eye(3))
#end = geometry.to_transformation_matrix([100, 50, 10], geometry.rz_matrix(np.pi))
end = geometry.to_transformation_matrix([100, 200, 10],np.eye(3))

frames = geometry.interpolate_frames(start, end, 30)
print(frames)
print("\n",type(frames[0]),"\n",frames[0],"\n",frames[15],"\n",frames[29])
# Sequential IK: each frame starts from the previous solution.
trajectory = robot.inverse_kinematics_trajectory_frame(
    frames,
    initial_position=current_joints,
    orientation_mode=None
)
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

