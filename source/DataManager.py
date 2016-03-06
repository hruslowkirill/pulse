import math 
xx = 0
def getCurrentValue():
    global xx
    xx = xx+0.1
    return math.sin(xx)
