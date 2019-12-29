import traceback
import math
import statistics

class Point():
    def __init__(self,args:list, result):
        self.args = args
        self.result = result

def newVal(x1,x2,y1,y2, iterations, gradientMagnitude = 0.5):
    assert(x2 != x1)
    m = (y2-y1)/(x2-x1)
    if m == 0:
        return (x2+x1)/2
    adjustment = math.atan(m/(iterations/10))*gradientMagnitude*(abs(x2-x1)**(1/3))
    return x1 - adjustment if y1 < y2 else x2 - adjustment
