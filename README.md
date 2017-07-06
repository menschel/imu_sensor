# imu_sensor
This project provides a python3 interface for fxas219002 gyroscope and fxos8700cq accelerometer,
i.e. the "NXP Precision 9DoF breakout" board by adafruit.
https://learn.adafruit.com/nxp-precision-9dof-breakout?view=all

Note: The gyroscope needs a software filter while the accelometer has an internal filter.

There is basic functionality to read a single or both sensors in parallel.

It was written for and tested on a Raspberry Pi 3.
