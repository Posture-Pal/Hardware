import time
import board
import busio
from adafruit_bno055 import BNO055

i2c = busio.I2C(board.SCL, board.SDA)

bno = BNO055(i2c)

if not bno.begin():
    print("No BNO055 detected, check wiring!")
    while True:
        pass

bno.set_ext_crystal_use(True)

while True:
    euler = bno.euler

    if euler is not None:
        print(f"Orientation: {euler[0]:.2f} {euler[1]:.2f} {euler[2]:.2f}")  # X, Y, Z axes

    time.sleep(1)
