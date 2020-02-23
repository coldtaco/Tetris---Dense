from tetris import Game
from tetrisFunctions import getScore, printBoard
import sys
import copy
import multiprocessing
from operator import itemgetter
import time
import numpy as np
linux = False
import pickle

class nnInput:

    def __init__(self):
        self.scoreBoard = np.zeros((4,10))

    def setBoard(self,board):
        self.board = board

    def setPiece(self,piece):
        self.piece = piece
    
    def setScore(self, vals):
        #score,(rotation,x)
        for val in vals:
            score , rx = val
            rotation, xVal = rx
            self.scoreBoard[rotation,xVal] = score
            #score higher the better

if sys.platform == "linux" or sys.platform == "linux2":
    import curses
    linux = False
d = {0 : 2, 1 : 1, 2 : 4, 3 : 4, 4 : 4, 5 : 2, 6 : 2}
#possible rotations for each block
def bestMove(board,piece):
    game = Game()
    combinations = []
    for rotation in range(d[piece]):#rotation
        leftest = 0
        rightest = 0
        game.rotation = rotation
        game.piece = piece
        orientation = game.orientation()
        for y,x in orientation:
            if game.marker[1] - x > leftest:
                leftest = game.marker[1] - x
            elif x - game.marker[1] > rightest:
                rightest = x - game.marker[1]
        #print(f'leftest = {leftest},rightest = {rightest}', end = '')
        assert(len(board[0]) == 10)
        for x in range(leftest,len(board[0])-rightest):
            combinations.append((board,rotation,x,piece,game))
    #results = map(multiWrapper,combinations)
    #return sorted(results,key = itemgetter(0))[-1]
    with multiprocessing.Pool() as pool:
        results = pool.map(multiWrapper,combinations)
    inp = nnInput()
    inp.setBoard(copy.deepcopy(board))
    inp.setPiece(piece)
    inp.setScore(results)
    with open('inputs/inputs.pkl','ab') as file:
        pickle.dump(inp,file)
    return sorted(results,key = itemgetter(0))[-1]

def multiWrapper(args):
    return checkReward(*args)

def checkReward(board,rotation,x,piece,game):
    game.cleared = 0
    game.board = copy.deepcopy(board)
    game.rotation = rotation
    game.marker[1] = x
    game.piece = piece
    assert game.cleared == 0
    game.train(4)
    score = getScore(game,0)
    return (score,(rotation,x))


def playGame():
    total = 0
    for x in range(10):
        piece = 0
        cleared = 0
        game = Game()
        if linux:
            stdscr = curses.initscr()
            pass
        game.train(6)
        while game.running:
            s1,m1 = bestMove(copy.deepcopy(game.board),game.piece)
            s2,m2 = bestMove(copy.deepcopy(game.board),game.hold)
            moves = moveOrder(m1,game) if s1 > s2 else moveOrder(m2,game,hold = True)
            for result in moves:
                if linux:
                    printBoard(game.train(result),stdscr)
                else:
                    game.play(result)
                    print(f'lines cleared {game.cleared},score {game.score}',end = '\r')
            '''game.rotation, game.marker[1] = m1
            game.play(4)'''
            piece += 1
        if linux:
            curses.endwin()
        total += game.score
        stats(game,piece)
    print(f'For a total of {total:.2f}!')

def stats(game,piece):
    print(f'Got a score of {game.score:.2f}')
    print(f'cleared {game.cleared} lines')
    print(f'placed {piece} pieces')
    open('algo.log','a').write(f'Got a score of {game.score:.2f}\ncleared {game.cleared} lines\nplaced {piece} pieces\n')


def moveOrder(bestMove,game,hold=False):
    moves = []
    if hold:
        moves.append(6)
    #[Keys.ARROW_LEFT,Keys.ARROW_RIGHT,Keys.ARROW_UP,Keys.ARROW_DOWN," ","z","c","a"]
    bestRotation, bestX = bestMove
    rotation = bestRotation
    if rotation == 1:
        moves.append(2)
    if rotation == 2:
        moves.append(7)
    if rotation == 3:
        moves.append(5)
    if bestX < game.marker[1]:#move left
        for x in range(game.marker[1] - bestX):
            moves.append(0)
    elif game.marker[1] < bestX:#move right
        for x in range(bestX - game.marker[1]):
            moves.append(1)
    moves.append(4)
    return moves

if __name__ == "__main__":
    multiprocessing.freeze_support()
    playGame()
