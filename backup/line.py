import numpy as np
from robot import robot
import matplotlib.pyplot as plt
print("start")

start = np.array([100, 180, 40], dtype=float)
goal = np.array([150, 100, 40], dtype=float)
n_points = 40

# Linear interpolation in Cartesian space
targets = np.linspace(start, goal, n_points)

trajectory = []  # list of joint-angle arrays

for target in targets:
    angles = robot.inverse_kinematics(target_position=list(target))

    if angles is None:
        print(f"IK failed at: {target}")
        continue

    trajectory.append(angles)

trajectory = np.array(trajectory)

print("Trajectory shape:", trajectory.shape)
print("First configuration:", np.degrees(trajectory[0]))
print("Last configuration:", np.degrees(trajectory[-1]))

fig = plt.figure(figsize=(9, 7))
ax = fig.add_subplot(111, projection="3d")

for angles in trajectory:
    ax.clear()
    robot.plot(angles, ax, target=list(goal))

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_xlim(-200, 200)
    ax.set_ylim(-200, 200)
    ax.set_zlim(0, 300)

    plt.pause(0.5)

plt.show()
