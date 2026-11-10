import numpy as np
from ikpy.utils import geometry
from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink
import matplotlib.pyplot as plt

L1 = 100
L2 = 95
L3 = 128

robot = Chain(
    name="merkur_beta_6",
    links=[
        OriginLink(),

        URDFLink(
            name="base",
            origin_translation=[0, 0, 0],
            origin_orientation=[0, 0, 0],
            rotation=[0, 1, 0],
            bounds=(-np.pi, np.pi),
        ),

        URDFLink(
            name="shoulder",
            origin_translation=[0, 0, 0],
            origin_orientation=[0, 0, 0],
            rotation=[0, 0, 1],
            bounds=(-np.pi / 2, np.pi / 2),
        ),

        URDFLink(
            name="elbow",
            origin_translation=[L1, 0, 0],
            origin_orientation=[0, 0, 0],
            rotation=[0, 0, 1],
            bounds=(-np.pi / 2, np.pi / 2),
        ),

        URDFLink(
            name="wrist",
            origin_translation=[L2, 0, 0],
            origin_orientation=[0, 0, 0],
            rotation=[0, 0, 1],
            bounds=(-np.pi / 2, np.pi / 2),
        ),

        URDFLink(
            name="pen",
            origin_translation=[L3, 0, 0],
            origin_orientation=[0, 0, 0],
            rotation=None,
            joint_type="fixed",
        ),
    ],
    active_links_mask=[False, True, True, True, True, False],
)
if __name__ == "__main__":
    print("start")

# Current joint configuration.
# Length must equal len(robot.links), here 6.
    current_joints = np.zeros(len(robot.links))

    start_position = np.array([100, 180, 40], dtype=float)
    goal_position = np.array([150, 100, 40], dtype=float)

    n_steps = 50

# Current end-effector frame.
    start_frame = robot.forward_kinematics(current_joints)

# Target frame. No orientation constraint.
    end_frame = geometry.to_transformation_matrix(
        target_position=goal_position,
        target_orientation=None
    )

# Straight-line position path, constant-speed orientation path.
    frames = geometry.interpolate_frames(
        start_frame,
        end_frame,
        n_steps=n_steps
    )

# Sequential IK: every frame starts from the previous joint solution.
    trajectory = robot.inverse_kinematics_trajectory_frame(
        frames,
        initial_position=current_joints,
        orientation_mode=None
    )

    trajectory = np.asarray(trajectory)

    print("Trajectory shape:", trajectory.shape)
    print("First configuration:", np.degrees(trajectory[0]))
    print("Last configuration:", np.degrees(trajectory[-1]))

# Show the largest motion between neighbouring frames.
    if len(trajectory) > 1:
        joint_steps = np.abs(np.diff(trajectory, axis=0))
        print("Largest joint step (deg):", np.degrees(joint_steps.max()))

# If your real robot class has a move_to() method:
# for joints in trajectory:
#     robot.move_to(joints)

# Visualization.
    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111, projection="3d")

    for joints in trajectory:
        ax.clear()

        robot.plot(
            joints,
            ax,
            target=goal_position.tolist()
        )

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.set_xlim(-200, 200)
        ax.set_ylim(-200, 200)
        ax.set_zlim(0, 300)

        plt.pause(0.05)

    plt.show()
