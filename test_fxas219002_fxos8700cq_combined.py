# test_fxas219002_fxos8700cq_combined.py
# (C) 2017 Patrick Menschel
from fxas219002 import FXAS21002
from fxos8700cq import FXOS8700CQ
import time

if __name__ == "__main__":
    FXOS8700CQ_obj = FXOS8700CQ()
    FXOS8700CQ_obj.startup()
    FXAS21002_obj = FXAS21002()
    FXAS21002_obj.startup()
    cnt = 0
    try:
        while cnt < 1000:
            #loop for 100 seconds just to get a feel about moving the sensor by hand
            gyro_status,gyro_xyz = FXAS21002_obj.get_values()
            accel_mag_status,accel_xyz,mag_xyz = FXOS8700CQ_obj.get_values()
            print("gyro (deg/s) {0:.2f} {1:.2f} {2:.2f}".format(*gyro_xyz))
            print("accel (mg) {0:.2f} {1:.2f} {2:.2f}".format(*accel_xyz))
            print("mag (uT) {0:.2f} {1:.2f} {2:.2f}".format(*mag_xyz))
            time.sleep(0.1)
            cnt += 1

    except KeyboardInterrupt:
        print("exit")
