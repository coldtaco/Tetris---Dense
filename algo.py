from tetris import Game
from tetrisFunctions import getScore, printBoard
import sys
import copy
linux = False
if sys.platform == "linux" or sys.platform == "linux2":
    import curses
    linux = True

def bestMove(board,piece):
    game = Game()
    bestScore = -10e6
    bestMove = None
    for rotation in range(4):#rotation
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
        for x in range(0+leftest,len(board[0])-rightest):
            game.cleared = 0
            game.board = copy.deepcopy(board)
            game.rotation = rotation
            game.marker[1] = x
            game.piece = piece
            assert game.cleared == 0
            game.train(4)
            score = getScore(game,0)
            if score > bestScore:
                bestScore = score
                bestMove = (rotation,x)
    return (bestScore,bestMove)

def playGame():
    for x in range(1):
        piece = 0
        cleared = 0
        game = Game()
        if linux:
            stdscr = curses.initscr()
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
            piece += 1
        if linux:
            curses.endwin()
        print(f'Got a score of {game.score:.2f}')
        print(f'cleared {game.cleared} lines')
        print(f'placed {piece} pieces')

def moveOrder(bestMove,game,hold=False):
    moves = []
    if hold:
        moves.append(6)
    #[Keys.ARROW_LEFT,Keys.ARROW_RIGHT,Keys.ARROW_UP,Keys.ARROW_DOWN," ","z","c","a"]
    bestRotation, bestX = bestMove
    if bestX < game.marker[1]:#move left
        for x in range(game.marker[1] - bestX):
            moves.append(0)
    elif game.marker[1] < bestX:#move right
        for x in range(bestX - game.marker[1]):
            moves.append(1)
    rotation = bestRotation
    if rotation == 1:
        moves.append(2)
    if rotation == 2:
        moves.append(7)
    if rotation == 3:
        moves.append(5)
    moves.append(4)
    return moves

playGame()