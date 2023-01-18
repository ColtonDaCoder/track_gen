import matplotlib.pyplot as plt
import math
import numpy as np

#point class for path class
#holds array of [x,y] for r and v
class Point():
    def __init__(self, r):
        self.r = r
    #r is position [x,y]
    #v is velocity [vx, vy]
    def __init__(self, r: list, v: list):
        self.r = r
        self.v = v

class Path():
    def __init__(self,track_width):
        self.points = []
        self.track_width = track_width

    def combine(track_width, paths):
        full_path = Path(track_width)
        full_path.endpoint = paths[-1].endpoint
        full_path.full_set = []
        for path in paths:
            full_path.full_set.extend(path.full_set.tolist())
        return full_path

 
    def append(self, point: Point):
        self.points.append(point)

    def track(self):
        A = np.array([[0,-1],[1,0]])
        self.full_set = []
        for point in self.points:
            U = np.divide(point.v, math.sqrt(point.v[0]**2 + point.v[1]**2))
            T = A @ np.array(U)
            N = T*self.track_width/2
            self.full_set.append(np.subtract(point.r, N))
            self.full_set.append(np.add(point.r, N))
            self.origin = Point(self.points[0].r, to_angle(self.points[0].v))
            self.endpoint = Point(self.points[-1].r, to_angle(self.points[-1].v))

    def getPoints(self,):
        list = [[point.r, point.v] for point in self.points]
        return list

    def rotate(self, origin: Point, degrees):
        angle = np.deg2rad(degrees)
        R = np.array([[np.cos(angle), -np.sin(angle)],
                      [np.sin(angle),  np.cos(angle)]])
        o = np.atleast_2d(origin)
        p = np.atleast_2d(self.full_set)
        self.full_set =  np.squeeze((R @ (p.T-o.T) + o.T).T)
        self.origin = Point(R @ (self.points[0].r - origin) + origin, to_angle(self.points[0].v) + degrees)
        self.endpoint = Point(R @ (self.points[-1].r - origin) + origin, to_angle(self.points[-1].v) + degrees)

    def vectors(self):
        x = []
        y = []
        u = []
        v = []
        for point in self.points:                
            x.append(point.r[0])
            y.append(point.r[1]) 
            u.append(point.v[0])
            v.append(point.v[1])
        plt.quiver(x, y, u, v)

    def plot(self):
        x = []
        y = []
        #self.full_set = self.full_set.astype(int)
        for i, set in enumerate(self.full_set):
            x.append(set[0])
            y.append(set[1])
        plt.plot(x, y, 'o') 



#returns distance between two points [x,y]
def distance(first, second):
    dif = np.subtract(first, second)
    return math.sqrt(dif[0]**2 + dif[1]**2)

#plots given points, ideally from path.full_set
def plot(sets):
    x = []
    y = []
    track = []
    for set in sets:
        track.extend(set.full_set)
        for point in set.full_set:
            x.append(point[0])
            y.append(point[1])
    max = np.amax(track)
    min = np.amin(track)
    plt.xlim(min, max)
    plt.ylim(min, max)
    print(min)
    plt.plot(0,0, 'go')
    #plt.axis('equal')
    plt.plot(x,y, 'o')
    plt.show()

#lambda function for track parametric equations
class function():
    def __init__(self, x=None, y=None, dx=None, dy=None):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

#converts [x,y] into angle
def to_angle(cord: list):
    return math.atan2(cord[1], cord[0])/math.pi*180

#used to create a path from a function f and other parameters
def create_path(track_width, length: list, origin: Point, f: function, is_reversed=False):
    if is_reversed:
       origin = reverse(origin)  
    path = Path(track_width)
    t_list = np.linspace(length[0], length[1], length[2]).tolist()
    zero_set = False
    true_zero = [0,0]
    for t in t_list:
        x = f.x(t) 
        y = f.y(t)
        dx = f.dx(t)
        dy = f.dy(t)
        if not zero_set:
            true_zero = [x,y]
            zero_set = True
        path.append(Point(np.subtract(np.add(origin.r,[x,y]), true_zero),[dx,dy]))

    path.track()
    angle =  origin.v-path.origin.v
    path.rotate(origin.r,angle)
    if is_reversed:
        path.endpoint = reverse(path.endpoint)
    #path.plot()
    return path

def reverse(point: Point):
    return Point(point.r, point.v - 180)

def example(width):

    circle = function()
    r = 5
    circle.x = lambda t : r*math.cos(np.deg2rad(t))
    circle.y = lambda t : r*math.sin(np.deg2rad(t))
    circle.dx = lambda t : -r*math.sin(np.deg2rad(t))
    circle.dy = lambda t : r*math.cos(np.deg2rad(t))
    initial = Point([0,0],0)
    A = create_path(width, [0,100, 5], initial, circle)

    line = function()
    line.x = lambda t : t
    line.y = lambda t : t
    line.dx = lambda t : 1
    line.dy = lambda t : 1
    B = create_path(width, [0,20,5], A.endpoint, line)

    C = create_path(width, [-45,45,5], B.endpoint, circle)

    D = create_path(width, [-90,20,5], C.endpoint, circle)

    E = create_path(width, [0, 10, 5], D.endpoint, line)

    circle = function()
    r = 5
    circle.x = lambda t : r*math.cos(np.deg2rad(t))
    circle.y = lambda t : r*math.sin(np.deg2rad(t))
    circle.dx = lambda t : -r*math.sin(np.deg2rad(t))
    circle.dy = lambda t : r*math.cos(np.deg2rad(t))
    F = create_path(width, [0, -180, 5], E.endpoint, circle, is_reversed=True)

    G = create_path(width, [0, 10, 5], F.endpoint, line, is_reversed=True)

    H = create_path(width, [0,200,5], G.endpoint, circle)

    I = create_path(width, [0, 20, 5], H.endpoint, line)
    J = create_path(width, [0, 45, 5], I.endpoint, circle)
    track = []
    track.extend(A.full_set.tolist())
    track.extend(B.full_set.tolist())
    track.extend(C.full_set.tolist())
    max = np.amax(track)
    min = np.amin(track)
    plt.xlim(min, max)
    plt.ylim(min, max)
    plt.plot(0,0, 'go')
    plt.axis('equal')
    plt.show()

