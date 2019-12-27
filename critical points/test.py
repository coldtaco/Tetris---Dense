import traceback
import math
import statistics

class Point():
    def __init__(self,x,y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return f"({self.x}, {self.y})"

    

def gradient(p1,p2):
    assert p2[0] != p1[0], f"{str(p1)}, {str(p2)}"
    return (p2[1] - p1[1])/(p2[0] - p1[0])

pointsY = []
pointsX = []
testedX = []

def addPoint(point):
    #print(f"({point[0]}, {point[1]})")
    testedX.append(point[0])
    if not len(pointsY):
        pointsY.append(point)
        pointsX.append(point)
    else:
        ind = len(pointsY)
        for i,p in enumerate(pointsY):
            x,y = p
            if point[1] < y:
                ind = i 
                break
        pointsY.insert(ind,point)
        ind = len(pointsY)
        for i,p in enumerate(pointsX):
            x,y = p
            if point[0] < x:
                ind = i 
                break
        pointsX.insert(ind,point)

def findClosests():
    #print(str(pointsY[0][0]))
    for i,p in enumerate(pointsX):
        x,y = p
        if x == pointsY[0][0]:
            return i
        

def checkVal(upperBound, lowerBound, val):
    return not (val < upperBound or val > lowerBound)
    if val < upperBound or val > lowerBound:
        return False
    return True

gradientMagnitude = 0.01
def findLowest(upperBound, lowerBound, function, delta = 0.01 ,startingPoints = 3):
    step = (upperBound - lowerBound)/ (startingPoints - 1)
    for x in range(startingPoints):
        addPoint((lowerBound + step * x,function(lowerBound + step * x)))
    iterations = startingPoints
    while abs(pointsY[0][0] - pointsY[1][0]) > delta:
        iterations += 1
        #print(f"delta = {abs(pointsY[0][0] - pointsY[1][0])}")
        lowestXInd = findClosests()
        if lowestXInd == 0 or lowestXInd == len(pointsX)-1:
            s = "lowerBound" if lowestXInd == 0 else "upperBound"
            print(f"3 points took {iterations} iterations with error of {abs(pointsY[0][0] - pointsY[1][0])}")
            print(f"lowest point for 3 point method is ({pointsY[0][0]}, {pointsY[0][1]}), at the {s}")
            return pointsY[0][0]
        p1,p2 = pointsX[lowestXInd - 1], pointsX[lowestXInd + 1]
        m1,m2 = gradient(p1,pointsY[0]), gradient(p2,pointsY[0])
        newX = None
        if abs(m1) < abs(m2) :
            newX = pointsY[0][0] - m1*gradientMagnitude
        else:
            newX = pointsY[0][0] - m2*gradientMagnitude
        #print(f"gradient = {m1 if abs(m1) < m2 else abs(m2)}")
        if checkVal(p2[0], p1[0], newX):
            addPoint((newX,function(newX)))
        else:
            closerP = p1[0] if abs(m1) < abs(m2) else p2[0]
            #print(f"trying mid point between {pointsY[0][0]} and {closerP}")
            addPoint(((pointsY[0][0]+closerP)/2, function((pointsY[0][0]+closerP)/2)))
    print(f"3 points took {iterations} iterations with error of {abs(pointsY[0][0] - pointsY[1][0])}")
    print(f"lowest point for 3 point method is ({pointsY[0][0]}, {pointsY[0][1]})")
#check y value, if not 

def pointGradient(p1,p2):
    assert p2.x != p1.x, f"{str(p1)}, {str(p2)}"
    return (p2.y - p1.y)/(p2.x - p1.x)


def getNewX(p1,middle,p2,function,delta = 10e-6):
    if abs(p1.x - middle.x) < delta or abs(middle.x - p2.x) < delta:
        return middle
    m1,m2 = gradient(p1,middle), gradient(p2,middle)
    if abs(m1) < abs(m2) :
        newX = middle.x - m1*gradientMagnitude
    else:
        newX = middle.x - m2*gradientMagnitude
    if not (newX < p2[0] or newX > p1[0]):
        newY = function(newX)
        return getNewX()
        addPoint((newX,function(newX)))
    else:
        closerP = p1[0] if abs(m1) < abs(m2) else p2[0]
        addPoint(((pointsY[0][0]+closerP)/2, function((pointsY[0][0]+closerP)/2)))

def twoPoints(p1,p2,lowerBound, upperBound, function, delta = 10e-6):
    iterations = 0
    gradientMagnitude = 0.5
    while abs(p1.x - p2.x) > delta:
        iterations += 1
        m = pointGradient(p1,p2)
        if m == 0:
            p2 = Point((p1.x+p2.x)/2, function((p1.x+p2.x)/2))
        if p1.y < p2.y:
            p2 = Point(p1.x- m*gradientMagnitude, function(p1.x- m*gradientMagnitude))
        else:
            p1 = Point(p2.x- m*gradientMagnitude, function(p2.x- m*gradientMagnitude))
        #print(f"points are {p1}, {p2}")
    print(f"2 points took {iterations} iterations with error of {abs(p1.x - p2.x)}")
    return p1 if p1.y < p2.y else p2

def f(x):
    return x**2
    #return x**2 #- 5*x**3 + x**4

if __name__ == "__main__":
    try:
        x1, x2 = -99000,10000
        delta = 10e-6
        findLowest(x1,x2,f,startingPoints=4,delta = delta)
        print(f"lowest point for 2 point method is {twoPoints(Point(x1,f(x1)),Point(x2,f(x2)),x1,x2,f,delta = delta)}")
    except (Exception,KeyboardInterrupt) as e:
        traceback.print_exc()
        print(str(pointsY))
        x = []
        for _ in pointsY:
            if _ not in x:
                x.append(_)
        print(str(testedX))
        print(str(x))
        print(statistics.stdev(testedX))
        print(statistics.mean(testedX))