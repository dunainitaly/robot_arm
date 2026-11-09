import numpy as np
from robot import robot
import matplotlib.pyplot as plt


target = [150, 100, 40]

angles = robot.inverse_kinematics(
    target_position=target
)

print("Úhly kloubů:")
print(np.degrees(angles))

# Dopředná kinematika – kontrola
matrix = robot.forward_kinematics(angles)

print("Výsledná pozice:")
print(matrix[:3, 3])


fig = plt.figure(figsize=(9, 7))
ax = fig.add_subplot(111, projection="3d")

robot.plot(
    angles,
    ax,
    target=target
)

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

plt.show()
