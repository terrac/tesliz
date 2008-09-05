from math import sqrt

def distance(v1,v2):
    return sqrt(pow(v1.x - v2.x,2) +pow(v1.y - v2.y,2) +pow(v1.z - v2.z,2))

#trajectory