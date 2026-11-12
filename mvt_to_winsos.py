import math

def load_template():
    lines = []
    with open("temp.sos") as f:
        lines = f.readlines()
    return lines

def rad_to_sos(rad: float):
    if rad > math.py/2 or rad < 0:
        raise ValueError("rad outside operatable range")
    servo: float = rad/(math.pi /2)*255
    return int(servo)

def angles_to_sos(trajectory):
    with open(input("enter name: ")+".sos", "w") as f:
        f.writelines(load_template())
    