import traceback
import math
import statistics
def f(x):
    return (x**2-1)**6
    

def gradient(p1,p2):
    return (p2[1] - p1[1])/(p2[0] - p1[0])

pointsY = []
pointsX = []
testedX = []

def addPoint(point):
    print(f"({point[0]}, {point[1]})")
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
    currentLowest = None
    for i,p in enumerate(pointsX):
        x,y = p
        if x == pointsY[0][0]:
            return i
        

def checkVal(upperBound, lowerBound, val):
    if val < upperBound or val > lowerBound:
        return False
    return True

def findLowest(upperBound, lowerBound, function, delta = 0.01 ,startingPoints = 3):
    step = (upperBound - lowerBound)/ (startingPoints - 1)
    for x in range(startingPoints):
        addPoint((lowerBound + step * x,function(lowerBound + step * x)))
    while abs(pointsY[0][0] - pointsY[1][0]) > delta:
        '''if len(testedX) > 50:
            print("greater than 50")
            std = statistics.stdev(testedX)
            mean = statistics.mean(testedX)
            if std - mean > lowerBound:
                print("changed lower bound")
                input()
                lowerBound = std - mean
            if std + mean < upperBound:
                print("changed upper bound")
                input()
                upperBound = std + mean'''
        print(f"delta = {abs(pointsY[0][0] - pointsY[1][0])}")
        lowestXInd = findClosests()
        if lowestXInd == 0 or lowestXInd == len(pointsX)-1:
            s = "lowerBound" if lowestXInd == 0 else "upperBound"
            print(f"lowest is at {s}, x = {pointsY[0][1]}, with y = {pointsY[0][1]}")
            print(str(pointsY))
            return
        p1,p2 = pointsX[lowestXInd - 1], pointsX[lowestXInd + 1]
        m1,m2 = gradient(p1,pointsY[0]), gradient(p2,pointsY[0])
        newX = None
        if abs(m1) < abs(m2) :
            newX = pointsY[0][0] - m1
        else:
            newX = pointsY[0][0] - m2
        #print(f"gradient = {}")
        if checkVal(upperBound, lowerBound, newX):
            addPoint((newX,function(newX)))
        else:
            closerP = p1[0] if abs(m1) < abs(m2) else p2[0]
            print(f"trying mid point between {pointsX[0][0]} and {closerP}")
            addPoint(((pointsX[0][0]+closerP)/2, function((pointsX[0][0]+closerP)/2)))
    print(f"error = {abs(pointsY[0][0] - pointsY[1][0])}")
    print(f"lowest point of function is at x = {pointsY[0][0]}, with y = {pointsY[0][1]}")
try:
    findLowest(-.5,10,f,startingPoints=11)
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