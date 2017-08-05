# rotate.py
# (C) 2017 Patrick Menschel
# do the rotational magic to transfer magnetometer and accelerometer data
# to the "global frame" aka the "horizontal plane pointing north" coordinate system



import math
import numpy as np

def rotate_phi(x,phi):
    """rotate around the first axis aka X aka roll"""
    #rotational matrix
    r_phi = np.array([[1,             0,            0],
                      [0, math.cos(phi),math.sin(phi)],
                      [0,-math.sin(phi),math.cos(phi)]
                     ])
    #numpys function for matrix multiplication, can be substituted by "@" for python > 3.5
    res = r_phi.dot(x)
    return res


def rotate_theta(x,theta):
    """rotate around the second axis aka Y aka pitch"""
    #rotational matrix
    r_theta = np.array([[math.cos(theta),0,-math.sin(theta)],
                        [              0,1,               0],
                        [math.sin(theta),0, math.cos(theta)]
                       ])
    #numpys function for matrix multiplication, can be substituted by "@" for python > 3.5
    res = r_theta.dot(x)
    return res
    

def rotate_psi(x,psi):
    """rotate around the third axis aka Z aka yaw"""
    #rotational matrix
    r_psi = np.array([[ math.cos(psi),math.sin(psi),0],
                      [-math.sin(psi),math.cos(psi),0],
                      [             0,            0,1]
                     ])
    #numpys function for matrix multiplication, can be substituted by "@" for python > 3.5
    res = r_psi.dot(x)
    return res

def rotate_to_global_frame(accelxyz,magxyz):
    """rotate local frame to global frame
       e.g. figure out the direction where gravity points to
       iter and rotate two axis, x=roll,y=pitch accordingly
       figure out the north direction and rotate the last axis
       z=yaw
       Note: Python3 math functions work in radians, not in degrees!"""
    #roll depends on y and z part of accelerometer data, e.g. where earth gravity points to
    phi = math.atan2(accelxyz[1],accelxyz[2])

    #correct both vectors for roll along x axis
    accelxyz = rotate_phi(accelxyz,phi)
    magxyz = rotate_phi(magxyz,phi)

    #pitch depends on x and z part of accelerometer data,
    theta = math.atan2(-accelxyz[0],accelxyz[2])

    #correct both vectors for pitch along y axis
    accelxyz = rotate_theta(accelxyz,theta)
    magxyz = rotate_theta(magxyz,theta)
    #print("after correcting for pitch {0}".format(theta))
    #print(accelxyz,magxyz)
    #now we are horizontal aligned, so check which direction north is
    #yaw depends on -y and x, so calculate it
    psi = math.atan2(-magxyz[1],magxyz[0])
    #correct both vectors for yaw
    accelxyz = rotate_psi(accelxyz,psi)
    magxyz = rotate_psi(magxyz,psi)
    #print("after correcting for yaw {0}".format(psi))
    #print(accelxyz,magxyz)
    arcs = np.array([phi,theta,psi])
    return accelxyz,magxyz,arcs
    

    


if __name__ == "__main__":
    accelxyz =np.array([14.64,-39.528,1011.136])
    magxyz = np.array([19.8,-57.300000000000004,28.200000000000003])
    print("before")
    print(accelxyz,magxyz)
    accelxyz,magxyz,arcs = rotate_to_global_frame(accelxyz,magxyz)
    print("aligned for roll {0:4.1f} pitch {1:4.1f} yaw {2:4.1f} (deg)".format(*[math.degrees(x) for x in arcs]))
    print(accelxyz,magxyz)


    


