import numpy as np
import pandas as pd

def wellDot(row):
    _ = np.transpose([row])
    _1 = _[0:-2]
    _2 = _[1:-1]
    _3 = _[2:]
    trips = np.hstack([_1,_2,_3])
    return np.apply_along_axis(dotCalc,1,trips)

def dotCalc(trip):
    _ = np.array([1,2,1])
    return np.dot(trip,_)

def wellScore(col):
    col = col.tolist()
    well = 0
    for i in range(3,len(col)):
        trip = col[i-3:i]
        if trip == [0,0,0]:
            well += 1
    return well

def wells(board):
    firstRow = findFirstOccupiedRow(board)
    if len(board) - firstRow <= 3:
        return 0
    else:
        board = board[firstRow:len(board) - 1]
    board = np.array(board)
    _board = board - 1
    one = [[1]]*len(board)
    _board = np.hstack([one,_board,one])
    _board = np.apply_along_axis(wellDot,1,_board)
    board = np.add(_board, board) #add to ensure it is OUO instead of UOU as both return 0, after adding, UOU will not be 0
    wells = np.apply_along_axis(wellScore, 0 , board)
    return wells.sum()

def findFirstOccupiedRow(board):
    '''
    empty = [0]*10
    for i, row in zip(reversed(range(len(board))),reversed(board)):
        if row == empty:
            return i
    return 0
    '''
    for i,row in enumerate(board):
        if 2 not in row and 1 not in row:
            return i
    return len(board) - 1

def holes(board):
    hole = 0
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == 0 and y > 0 and (board[y-1][x] == 2 or board[y-1][x] == 3):
                hole += 1
                board[y][x] = 3
    return hole

#get uneveness by using standard distance of local columns to column
def distance(board):
    lowest = [len(board) for x in range(len(board[0]))]
    unchecked = list(range(len(board[0])))
    for y in range(len(board)):
        if len(unchecked) == 0:
            break
        for x in list(reversed(unchecked)):
            if board[y][x] == 2:
                unchecked.remove(x)
                lowest[x] = y
    diff = []
    lowest = np.array(lowest)
    return np.abs(lowest[0:-1] - lowest[1:]).sum()
    for x in range(2,len(board[0])-2):
        tup = lowest[x-2:x+3]
        diff.append(np.average(np.abs(tup - tup[2])))
    diff = np.array(diff)*5//3
    return diff.sum()

def rowTransitions(board):
    board = np.array(board)
    _board = board - 1
    one = [[1]]*20
    _board = np.hstack([one,_board,one])/2
    rowTrans = 0
    for col in range(len(_board[0])-1):
        rowTrans += np.sum(_board[:,col] * _board[:,col+1])
    return rowTrans

def colTransitions(board):
    board = np.array(board)
    colTrans = 0
    for row in range(len(board)-1):
        colTrans += np.dot(board[row,:], board[row+1,:])
    return colTrans