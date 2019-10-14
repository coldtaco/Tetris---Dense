import scoring
import pickle

def printBoard(board,stdscr):
    for i,l in enumerate(board):
        stdscr.addstr(i,0,l)
    stdscr.refresh()

def getScore(game, cleared):
    board = game.board
    wells = scoring.wells(board)
    holes = scoring.holes(board)
    distance = scoring.distance(board)
    lastHeight = game.lastHeight
    cleared = game.cleared - cleared
    rowTrans = scoring.rowTransitions(board)
    colTrans = scoring.colTransitions(board)
    return 8*cleared - wells - 4*holes - distance - (19 - lastHeight)
    return cleared - wells - 4*holes - distance - (19 - lastHeight) - rowTrans - colTrans