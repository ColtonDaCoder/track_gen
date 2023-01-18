import track_tools as tools
import numpy as np
import math
import random

track_width = 5

def curve(origin, angle, is_reversed=False, r=5):
    f = tools.function(
            x=lambda t : r*math.cos(np.deg2rad(t)),
            y=lambda t : r*math.sin(np.deg2rad(t)),
            dx=lambda t : -r*math.sin(np.deg2rad(t)),
            dy=lambda t : r*math.cos(np.deg2rad(t)))
    if is_reversed:
        return tools.create_path(track_width, [0,-angle, int(angle*r/120)], origin, f, is_reversed=True)
    else:
        return tools.create_path(track_width, [0,angle, int(angle*r/120)], origin, f)



def straight(origin, length):
    f = tools.function(
            lambda t : t,
            lambda t : t,
            lambda t : 1,
            lambda t : 1)
    return tools.create_path(track_width, [0,length,int(length/2)], origin, f)

def long_straight(origin):
    A = hairpin(origin)
    length = random.randrange(45, 60, 1)
    B = straight(A.endpoint, length)
    C = hairpin(B.endpoint, is_reversed=True)
    return tools.Path.combine(5, [A, B, C])

def short_straight(origin):
    A = wide_turn(origin)
    length = random.randrange(30, 45, 1)
    B = straight(A.endpoint, length)
    C = wide_turn(B.endpoint, is_reversed=True)
    return tools.Path.combine(5, [A, B, C])


def hairpin(origin, is_reversed=False):
    angle = random.randrange(180, 230, 1)
    return curve(origin, angle, is_reversed)

def constant_turn(origin, is_reversed=False):
    angle = 45
    r = random.randrange(23*2,45*2, 1)
    return curve(origin, angle, is_reversed=False, r=r)

def wide_turn(origin, is_reversed=False):
    angle = random.randrange(100,200, 10)
    return curve(origin, angle, is_reversed)

initial = tools.Point([0,0],0)
A = straight(initial,2)
B = long_straight(A.endpoint)
C = curve(B.endpoint, 45)
D = short_straight(C.endpoint)

#tools.plot([A, B, C, D])
