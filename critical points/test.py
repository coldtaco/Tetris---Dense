import traceback
import math
import statistics
import random

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
    return not (val > upperBound or val < lowerBound)
    if val < upperBound or val > lowerBound:
        return False
    return True


def findLowest(upperBound, lowerBound, function, delta = 0.01 ,startingPoints = 3):
    gradientMagnitude = 0.05
    step = (upperBound - lowerBound)/ (startingPoints - 1)
    for x in range(startingPoints):
        addPoint((lowerBound + step * x,function(lowerBound + step * x)))
    iterations = startingPoints
    X = []
    Y = []
    while abs(pointsY[0][0] - pointsY[1][0]) > delta:
        print(iterations,gradientMagnitude)
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
        print(p2[0],p1[0],newX)
        if checkVal(p2[0], p1[0], newX):
            addPoint((newX,function(newX)))
            X.append(newX)
            Y.append(function(newX))
        else:
            closerP = p1[0] if abs(m1) < abs(m2) else p2[0]
            print(f"trying mid point between {pointsY[0][0]} and {closerP}")
            addPoint(((pointsY[0][0]+closerP)/2, function((pointsY[0][0]+closerP)/2)))
            X.append((pointsY[0][0]+closerP)/2)
            Y.append(function((pointsY[0][0]+closerP)/2))
    plt.plot(X,Y,'ro-')
    print(X)
    print(f"3 points took {iterations} iterations with error of {abs(pointsY[0][0] - pointsY[1][0])}")
    print(f"lowest point for 3 point method is ({pointsY[0][0]}, {pointsY[0][1]})")
#check y value, if not 

def pointGradient(p1,p2):
    assert p2.x != p1.x, f"{str(p1)}, {str(p2)}"
    return (p2.y - p1.y)/(p2.x - p1.x)


def twoPoints(p1,p2,lowerBound, upperBound, function, delta = 10e-6):
    iterations = 0
    gradientMagnitude = .6
    X = []
    Y = []
    try:
        while abs(p1.x - p2.x) > delta :
            #print(f"points are {p1}, {p2}")
            iterations += 1
            m = pointGradient(p1,p2)
            if abs(m) < 10e-6:
                p2 = Point((p1.x+p2.x)/2, function((p1.x+p2.x)/2))
                print("trying mid point")
                continue
            #adjustment = math.atan(m/(iterations**(.5)/3))*gradientMagnitude*(abs(p2.x-p1.x)**(1/3))#/(upperBound - lowerBound))*abs(p2.x-p1.x)
            adjustment = math.atan(m/(iterations/10))*gradientMagnitude*(abs(p2.x-p1.x)**(1/3))
            #print(m)
            #print(f"adjustment = {math.tanh(m)} * {gradientMagnitude} * {abs(p2.x-p1.x)**(1/3)} = {adjustment}")
            if p1.y < p2.y:
                p2 = Point(p1.x- adjustment, function(p1.x- adjustment))
                '''if (p2.x < lowerBound) or p2.x > upperBound:
                    break'''
                X.append(p2.x), Y.append(p2.y)
            else:
                p1 = Point(p2.x- adjustment, function(p2.x- adjustment))
                '''if (p1.x < lowerBound) or p1.x > upperBound:
                    break'''
                X.append(p1.x), Y.append(p1.y)
            #print(f"points are {p1}, {p2}")
            #print("")
    except:
        pass
    plt.plot(X,Y,"bo-")
    print(abs(p1.x - p2.x) > delta ,p1.x >= lowerBound , p2.x <= upperBound)
    print(f"2 points took {iterations} iterations with error of {abs(p1.x - p2.x)}")
    return p1 if p1.y < p2.y else p2

def f(x):
    #return math.atan(x)
    return x**2 - 5*x**3 + 2*x**4

def binary(lowerBound,upperBound,function, delta=10e-6):
    r = function(upperBound)
    iterations = 0
    X=[]
    Y=[]
    while abs(lowerBound - upperBound) > delta:
        print(lowerBound,upperBound)
        r1,r2 = function(lowerBound), function(upperBound)
        if r1 < r2:
            upperBound = (lowerBound + upperBound)/2
            X.append(upperBound)
            Y.append(function(upperBound))
        else:
            lowerBound = (lowerBound + upperBound)/2
            X.append(lowerBound)
            Y.append(function(lowerBound))
        iterations += 1
    plt.plot(X,Y,'m-')
    print(f"lowest point for binary point method is {upperBound} or {lowerBound}")
    print(f"binary points took {iterations} iterations with error of {abs(upperBound - lowerBound)}")

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import numpy as np
    try:
        x1, x2 = -9,10
        x = np.linspace(int(x1),int(x2),int(x2 - x1)*10)
        y = np.array([f(_) for _ in x])
        plt.plot(x,y,'k')
        delta = 10e-6
        #findLowest(x1,x2,f,startingPoints=3,delta = delta)
        print(f"lowest point for 2 point method is {twoPoints(Point(x1,f(x1)),Point(x2,f(x2)),x1,x2,f,delta = delta)}")
        binary(x1,x2,f)
        plt.show()
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
