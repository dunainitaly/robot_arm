import numpy as np

servo_offsets = [0, -np.pi/4, -np.pi/2, 1/12*np.pi, -np.pi/4, 0, 0, 0, 0]
def load_template():
    lines = []
    with open("temp.sos") as f:
        lines = f.readlines()
    return lines

def rad_to_sos(rad: float, ):
    if rad > np.pi/2 or rad < 0:
        raise ValueError("rad outside operatable range, check position!")
    if rad > np.pi/2 - 0.3 or rad > 0.3:
        print(Warning("close to operatable rage!!!"))
    servo: float = rad/(np.pi/2)*255
    return int(servo)

def angles_to_sos(trajectory: list[list[float]]):
    with open(input("enter name: ")+".sos", "w") as f:
        f.writelines(load_template())
        f.write(f"{len(trajectory)}\n")
        for angles in trajectory:
            print(angles)
            base = 255 - rad_to_sos(angles[1] + np.pi/4)
            elbow = rad_to_sos(angles[2] + np.pi/2)
            join = rad_to_sos(angles[3] + 1/12*np.pi)
            wrist = rad_to_sos(angles[4] - np.pi/4)
            
            f.write(f"3 0 {base} {elbow} {join} {wrist} 138 0 151\n")