import matplotlib.pyplot as plt
import math
import numpy as np

class Constraints():
    def __init__(self, Xi, Yi, Xmax, Ymax, angle):
        self.Xi = Xi
        self.Yi = Yi
        self.Xmax = Xmax
        self.Ymax = Ymax
        self.angle = angle
class Path():
    def __init__(self,track_width):
        self.points = []
        self.track_width = track_width
 
    def append(self, point):
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

    def rotate(self, origin, degrees):
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
        for i, set in enumerate(self.full_set):
            x.append(set[0])
            y.append(set[1])
        plt.plot(x, y, 'o')

    



class Point():
    def __init__(self, r):
        self.r = r
    #r is position [x,y]
    #v is velocity [vx, vy]
    def __init__(self, r, v):
        self.r = r
        self.v = v



def distance(first, second):
    dif = np.subtract(first, second)
    return math.sqrt(dif[0]**2 + dif[1]**2)


def plot(points):
    x = []
    y = []
    for point in points:
        x.append(point[0])
        y.append(point[1])
    plt.plot(x,y)

class function():
    def __init__(self,):
        self.x = None
        self.y = None
        self.dx = None
        self.dy = None
def to_angle(cord):
    return math.atan2(cord[1], cord[0])/math.pi*180

def create_path(track_width, length, origin, f):
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
    print(origin.v)
    print(path.origin.v)
    path.rotate(origin.r,angle)
    path.plot()
    return path

def reverse(point):
    return Point(point.r, point.v - 180)

circle = function()
r = 10
circle.x = lambda t : r*math.cos(np.deg2rad(t))
circle.y = lambda t : r*math.sin(np.deg2rad(t))
circle.dx = lambda t : -r*math.sin(np.deg2rad(t))
circle.dy = lambda t : r*math.cos(np.deg2rad(t))
initial = Point([0,0],0)
A = create_path(5, [0,100, 90], initial, circle)

line = function()
line.x = lambda t : t
line.y = lambda t : t
line.dx = lambda t : 1
line.dy = lambda t : 1
B = create_path(5, [0,20,20], A.endpoint, line)

C = create_path(5, [-45,45,10], B.endpoint, circle)

D = create_path(5, [-90,20,10], C.endpoint, circle)

E = create_path(5, [0, 10, 10], D.endpoint, line)

circle = function()
r = 10
circle.x = lambda t : r*math.cos(np.deg2rad(t))
circle.y = lambda t : r*math.sin(np.deg2rad(t))
circle.dx = lambda t : -r*math.sin(np.deg2rad(t))
circle.dy = lambda t : r*math.cos(np.deg2rad(t))
F = create_path(5, [0, -180, 10], reverse(E.endpoint), circle)

G = create_path(5, [0, 20, 10], reverse(F.endpoint), line)


track = []
track.append(A.full_set)
#track.append(B[0])
#track.append(C[0])
max = np.amax(track)
min = np.amin(track)

plt.xlim(min, max)
plt.ylim(min, max)
plt.plot(0,0, 'go')
plt.axis('equal')
plt.show()
exit()
