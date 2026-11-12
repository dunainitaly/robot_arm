import math

servo_offsets = [0, 0, 0, 0, 0, 0, 0, 0]

def load_template():
    lines = []
    with open("temp.sos") as f:
        lines = f.readlines()
    return lines

def rad_to_sos(rad: float):
    rad -= math.pi/2
    if rad > math.pi or rad < 0:
        raise ValueError("rad outside operatable range, check position!")
    if rad > math.pi-0.3 or rad > 0.3:
        print(Warning("close to operatable rage!!!"))
    servo: float = rad/(math.pi)*255
    return int(servo)

def angles_to_sos(trajectory: list[list[float]]):
    with open(input("enter name: ")+".sos", "w") as f:
        f.writelines(load_template())
        f.write(f"{len(trajectory)}\n")
        print(angles, servo_offsets)
        for angles in trajectory:
            f.write("15 ")
            for offset, angle in zip(servo_offsets, angles):
                f.write(f"{rad_to_sos(angle + offset)} ")
        f.write("\n")
        input()