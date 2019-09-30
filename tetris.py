import numpy as np
import copy
import traceback
import sys
import pandas as pd
#import curses
class Game:
    def __init__(self):
        self.bag = self.newBag()
        board = [0 for x in range(10)]
        board = [list(board) for x in range(20)]
        self.board = board
        self.piece = self.bag.pop()
        self.rotation = 0
        self.marker = [-2,5]
        self.hold = None
        self.fall = False
        self.touched  = 0
        self.cleared = 0
        self.running = True
        self.coords = self.orientation()
        self.score = 0
        self.b2b = False
        self.held = False
        self.hiddenScore = 0

    def train(self,inp):
        self.play(inp,False)
        return self.drawBoard(False)

    def checkValid(self):#corrects position of tetrimino (out of bounds or overlapping)
        changed = False
        for i,z in enumerate(self.coords):
            y,x = z
            if changed:
                y,x = self.coords[i]
            if y < 0:
                continue
            if x < 0:
                while x < 0:
                    self.marker[1] += 1
                    self.coords = self.orientation()
                    y,x = self.coords[i]
                    changed = True
            elif x>9:
                while x>9:
                    self.marker[1] -= 1
                    self.coords = self.orientation()
                    y,x = self.coords[i]
                    changed = True
            if y > 19:
               while y > 19:
                    self.marker[0] -= 1
                    self.coords = self.orientation()
                    y,x = self.coords[i]
                    changed = True
            if self.board[y][x] == 2:
                if y > self.marker[0] and (y > 0):
                    while self.board[y][x] == 2  and (y > 0):
                        if self.marker[0] < 1:
                            break
                        self.marker[0] -= 1
                        self.coords = self.orientation()
                        y,x = self.coords[i]
                        changed = True
                if x < self.marker[1]:#touching to the left
                    if x > 9:
                        break
                    while self.board[y][x] == 2:
                        self.marker[1] += 1
                        self.coords = self.orientation()
                        y,x = self.coords[i]
                        changed = True
                elif x > self.marker[1]:#touching to the right
                    if x < 0:
                        break
                    while self.board[y][x] == 2:
                        self.marker[1] -= 1
                        self.coords = self.orientation()
                        y,x = self.coords[i]
                        changed = True
        return
    
    def overlapCheck(self):#checks if there is overlap (does not correct). Used for stopping certain moves
        for i,z in enumerate(self.orientation()):
            y,x = z
            if x < 0:
                return True
            elif x > 9:
                return True
            if y < 0:
                continue
            if y > 19:
                return True
            if self.board[y][x] == 2:
                return True
        return False

    def newBag(self):#creatse a new bag of tetriminos
        bag = list(range(7))
        bag = bag*2
        np.random.shuffle(bag)
        return bag
            
    def clear(self):#clears lines
        linesCleared = 0
        for i in range(len(self.board)):
            if 0 not in self.board[19-i] and 1 not in self.board[19-i]:
                linesCleared += 1
            else:
                self.board[19-i-linesCleared] = self.board[19-i]
            pass
        self.b2b = False if linesCleared == 0 else True
        if linesCleared == 1:
            self.score += 150 if self.b2b else 100
        elif linesCleared == 2:
            self.score += 450 if self.b2b else 300
        elif linesCleared == 3:
            self.score += 750 if self.b2b else 500
        elif linesCleared == 4:
            self.score += 1200 if self.b2b else 800
        self.cleared += linesCleared

    def endGame(self):
        self.running = False
        hole = 0
        for y in range(len(self.board)):
            for x in range(len(self.board[0])):
                if self.board[y][x] == 0 and y > 0 and self.board[y-1][x] == 2:
                    hole += 1
        self.hiddenScore -= hole


    def setPiece(self):#sets tetrimino in place and resets some info used for tracking it
        for y,x in self.coords:
            if y < 0:
                self.endGame()
                return
            self.board[y][x] = 2
        self.clear()
        if len(self.bag) == 0:
            self.bag = self.newBag()
        self.piece = self.bag.pop()
        self.rotation = 0
        self.touched = 0
        self.marker = [-2,5]
        self.held = False
        self.coords = self.orientation()
        self.running = not self.overlapCheck()
                
    def play(self,intake,prin = True):
        try:
            if self.running:
                self.move(intake)
                if prin:
                    self.drawBoard()
            else:
                print("GAME OVER")
        except Exception as e:
            print(e)
            traceback.print_exc()
            print(self.marker)
            print(self.coords)
            crash = open("crash.log",'w')
            self.dBoard(crash)
            crash.write(str(e))
            crash.write(traceback.format_exc())
            crash.close()
            sys.exit()
    
    def hardDrop(self):
            orientation = self.orientation()
            lowest = {}
            lowestPosition = -2
            for y,x in orientation:
                if x in lowest:
                    lowest[x] = y - self.marker[0] if lowest[x] < y - self.marker[0] else lowest[x]
                else:
                    lowest[x] = y - self.marker[0]
                lowestPosition = y if lowestPosition < y else lowestPosition
            lowestPosition -= self.marker[0]
            keys = list(lowest.keys())
            y_ = self.marker[0]
            while y_ < 0:
                for y in lowest.values():
                    if y < 0:
                        for x in lowest:
                            lowest[x] += 1
                y_ += 1
            for y in range(len(self.board)+2):
                if lowest[x] + y < 0:
                    continue
                for x in keys:
                    if self.board[lowest[x]+y][x] == 2:
                        self.score += (y - self.marker[0] - 1)*2
                        self.marker[0] = y - 1
                        return
                    if lowest[x]+y >= 19 :
                        self.score = (19 - lowestPosition- self.marker[0])*2
                        self.marker[0] = 19 - lowestPosition
                        return

    def dBoard(self,crash):
        tempBoard = copy.deepcopy(self.board)
        string = ""
        for y in tempBoard:
            for x in y:
                if x == 2:
                    string += "#"
                    print('#',end='')
                elif x == 1:
                    string += "0"
                    print('0',end='')
                else:
                    string += " "
                    print(" ",end='')
            string += '\n'
            print("\n",end='')
        crash.write(string)
        crash.write(str(self.coords))
        crash.write(str(self.marker))
        crash.write(str(self.piece))
        crash.write(str(self.orientation))

    def move(self, intake):
        #[Keys.ARROW_LEFT,Keys.ARROW_RIGHT,Keys.ARROW_UP,Keys.ARROW_DOWN," ","z","c","a"]
        # 0 : "I", 1 : "O", 2 : "T", 3 : "J", 4 : "L", 5 : "S", 6 : "Z"
        if intake == 0 :#left
            self.marker[1] -= 1
            if self.overlapCheck():
                self.marker[1] += 1
        elif intake == 1:#right
            self.marker[1] += 1
            if self.overlapCheck():
                self.marker[1] -= 1
        elif intake == 2:#rotate clockwise
            self.rotation += 1
        elif intake == 3:#down
            self.marker[0] += 1
            self.score += 1
            if self.overlapCheck():
                self.score -= 1
                self.marker[0] -= 1
                self.checkValid()
                self.setPiece()
                return
        elif intake == 4:#hard drop
            self.hardDrop()
            self.coords = self.orientation()
            self.setPiece()
            return
        elif intake == 5:#rotate counterclockwise
            self.rotation -= 1
        elif intake == 6:#hold
            if not self.held:
                held = True
                hold = self.hold
                if hold == None:
                    self.hold = self.piece
                    if len(self.bag) == 0:
                        self.bag = self.newBag()
                    self.piece = self.bag.pop()
                else:
                    self.hold = self.piece
                    self.piece = hold
                    self.marker = [0,5]
            elif intake == 7:#rotate 180
                self.rotation += 2
        #mechanism for slowly falling, time based solution is inefficient for ML
        self.coords = self.orientation()
        touching = self.checkTouching()
        if self.fall and not touching:
            self.marker[0] += 1
            if self.overlapCheck():
                self.marker[0] -= 1
            self.coords = self.orientation()
            touching = self.checkTouching()
        self.fall = not self.fall
        if(touching):
            #print(f'touched {self.touched} times')
            self.touched += 1
        if (self.touched == 3):
            for y,x in self.coords:
                if y < 0:
                    #print(y,x)
                    self.running =  False
                    return
            self.checkValid()
            self.setPiece()
            return
        self.checkValid()

    def checkTouching(self):#checks if tetrimino is touching something form the bottom
        for y,x in self.coords:
            try:
                if y + 1 < 0:
                    continue
                if y == 19:
                    return True
                if self.board[y+1][x] == 2:
                    return True
            except IndexError as e:
                continue
        return False

    def drawBoard(self,prin = True):
        tempBoard = copy.deepcopy(self.board)
        coords = self.orientation() 
        for y,x in coords:
            if y < 0:
                continue
            if tempBoard[y][x] == 2:
                continue
            tempBoard[y][x] = 1
        if prin:
            for y in tempBoard:
                for x in y:
                    if x == 2:
                        print('#',end='')
                    elif x == 1:
                        print('0',end='')
                    else:
                        print(" ",end='')
                print('\n',end='')
        else:
            strings = []
            for y in tempBoard:
                string = ""
                for x in y:
                    if x == 2:
                        string +='■'
                    elif x == 1:
                        string +='#'
                    else:
                        string +=' '
                strings.append(string)
            string += f"Lines cleared : {self.cleared}\n"
            string += f"Score : {self.score}\n"
            return strings

    def orientation(self):#return list of tuples of coordinates of tetrimino when drawn
        x = self.marker[0]
        y = self.marker[1]
        piece = self.piece
        if piece == 0:
            if self.rotation % 4 == 0:
                return ((x-1,y),(x,y),(x+1,y),(x+2,y))
            elif self.rotation % 4 == 1:
                return ((x,y-1),(x,y),(x,y+1),(x,y+2))
            elif self.rotation % 4 == 2:
                return ((x-2,y),(x-1,y),(x,y),(x+1,y))
            elif self.rotation % 4 == 3:
                return ((x,y-2),(x,y-1),(x,y),(x,y+1))
        elif piece == 1:
            return ((x,y),(x,y+1),(x+1,y),(x+1,y+1))
        elif piece == 2:
            if self.rotation % 4 == 0:
                return ((x,y+1),(x,y),(x,y-1),(x-1,y))
            elif self.rotation % 4 == 1:
                return ((x-1,y),(x,y),(x+1,y),(x,y+1))
            elif self.rotation % 4 == 2:
                return ((x,y+1),(x,y),(x,y-1),(x+1,y))
            elif self.rotation % 4 == 3:
                return ((x-1,y),(x,y),(x+1,y),(x,y-1))
        elif piece == 3:
            if self.rotation % 4 == 0:
                return ((x-1,y+1),(x,y+1),(x,y),(x,y-1))
            elif self.rotation % 4 == 1:
                return ((x-1,y),(x,y),(x+1,y),(x+1,y+1))
            elif self.rotation % 4 == 2:
                return ((x+1,y-1),(x,y+1),(x,y),(x,y-1))
            elif self.rotation % 4 == 3:
                return ((x-1,y),(x,y),(x+1,y),(x-1,y-1))
        elif piece == 4:
            if self.rotation % 4 == 0:
                return ((x-1,y-1),(x,y+1),(x,y),(x,y-1))
            elif self.rotation % 4 == 1:
                return ((x-1,y),(x,y),(x+1,y),(x-1,y+1))
            elif self.rotation % 4 == 2:
                return ((x+1,y+1),(x,y+1),(x,y),(x,y-1))
            elif self.rotation % 4 == 3:
                return ((x-1,y),(x,y),(x+1,y),(x+1,y-1))
        elif piece == 5:
            #s
            if self.rotation % 4 == 0:
                return ((x,y-1),(x,y),(x+1,y),(x+1,y+1))
            elif self.rotation % 4 == 1:
                return ((x-1,y+1),(x+1,y),(x,y),(x,y+1))
            elif self.rotation % 4 == 2:
                return ((x,y),(x-1,y),(x,y+1),(x-1,y-1))
            elif self.rotation % 4 == 3:
                return ((x+1,y-1),(x,y-1),(x-1,y),(x,y))
        elif piece == 6:
            #z
            if self.rotation % 4 == 0:
                return ((x+1,y-1),(x+1,y),(x,y),(x,y+1))
            elif self.rotation % 4 == 1:
                return ((x-1,y),(x,y),(x,y+1),(x+1,y+1))
            elif self.rotation % 4 == 2:
                return ((x,y-1),(x,y),(x-1,y),(x-1,y+1))
            elif self.rotation % 4 == 3:
                return ((x-1,y-1),(x,y-1),(x,y),(x+1,y))



