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
    changeCleared = game.cleared - cleared
    open('scores','a').write(str(8*changeCleared - wells - 4*holes - distance - (19 - lastHeight))+'\n')
    return 80*changeCleared - wells - 4*holes - distance - 10*(19 - lastHeight)