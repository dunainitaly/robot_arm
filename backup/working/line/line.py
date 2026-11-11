import numpy as np
from ikpy.utils import geometry
from robot import robot

from ikpy.utils import geometry

# Current joint configuration: one value per link, including fixed links.
current_joints = np.zeros(len(robot.links))

start_position = np.array([100, 180, 40], dtype=float)
goal_position = np.array([150, 100, 40], dtype=float)

# No orientation constraint.
target_orientation = None

n_steps = 50

# Current end-effector frame.
start_frame = robot.forward_kinematics(current_joints)

# Target 4x4 homogeneous transformation matrix.
# Use positional arguments.
end_frame = geometry.to_transformation_matrix(
    goal_position,
    target_orientation
)

# Straight-line position path and constant-speed orientation path.
frames = geometry.interpolate_frames(
    start_frame,
    end_frame,
    n_steps=n_steps
)

# Sequential IK: each frame starts from the previous solution.
trajectory = robot.inverse_kinematics_trajectory_frame(
    frames,
    initial_position=current_joints,
    orientation_mode=None
)

trajectory = np.asarray(trajectory)
