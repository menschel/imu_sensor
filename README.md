# imu_sensor
This project provides a python3 interface for fxas219002 gyroscope and fxos8700cq accelerometer,
i.e. the "NXP Precision 9DoF breakout" board by adafruit.
https://learn.adafruit.com/nxp-precision-9dof-breakout?view=all

Note: The gyroscope needs a software filter while the accelometer has an internal filter.

There is basic functionality to read a single or both sensors in parallel.

It was written for and tested on a Raspberry Pi 3 and a Raspberry Zero W.

# Some measurements of the standard deviation.

fxas219002 gyro

x	1.0627007671956068

y	0.8387527442221671

z	0.391810523916495

fxos8700cq accel

x	10.865536710167609

y	34.90547711749545

z	12.529244280482354

fxos8700cq mag

x	0.9219213632409223

y	0.8582418074179329

z	1.1792790170269292
