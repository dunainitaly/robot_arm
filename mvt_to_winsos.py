import numpy as np

servo_offsets = [0, -np.pi/4, -np.pi/2, 1/12*np.pi, -np.pi/4, 0, 0, 0]

def load_template():
    lines = []
    with open("temp.sos") as f:
        lines = f.readlines()
    return lines

def rad_to_sos(rad: float):
    if rad > np.pi or rad < 0:
        raise ValueError("rad outside operatable range, check position!")
    if rad > np.pi-0.3 or rad > 0.3:
        print(Warning("close to operatable rage!!!"))
    servo: float = rad/(np.pi)*255
    return int(servo)

def angles_to_sos(trajectory: list[list[float]]):
    with open(input("enter name: ")+".sos", "w") as f:
        f.writelines(load_template())
        f.write(f"{len(trajectory)}\n")
        for angles in trajectory:
            f.write("15 ")
            print(angles, servo_offsets)
            for offset, angle in zip(servo_offsets, angles):
                print(angle)
                f.write(f"{rad_to_sos(angle - offset)} ")
            f.write("\n")