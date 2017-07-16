# simple_kalman.py
# (C) 2017 Patrick Menschel
# Collection of functions needed to implement a simple kalman filter

import math

def calc_std_deviation(vals):
    return math.sqrt(sum([val*val for val in vals])/len(vals))
