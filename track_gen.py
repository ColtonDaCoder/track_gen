import patterns as pats
import random
import track_tools as tools

patterns = {
        "long": lambda o: pats.long_straight(o),
        "short": lambda o: pats.short_straight(o),
        #"CURVE": lambda o, angle: pats.curve(o, angle)
        "constant turn": lambda o: pats.constant_turn(o)
        }

paths = [list(patterns.keys())[random.randint(0,2)] for i in range(7)]
track = []
initial = tools.Point([0,0],0)
next_origin = initial
for path in paths:
    next_path = patterns.get(path)(next_origin)
    track.append(next_path)
    next_origin = next_path.endpoint

tools.plot(track)



