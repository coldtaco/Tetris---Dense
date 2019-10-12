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
            game.board = copy.deepcopy(board)
            game.rotation = rotation
            game.marker[1] = x
            game.piece = piece
            game.train(4)
            score = getScore(game,0)
            if score > bestScore:
                bestScore = score
                bestMove = (rotation,x)
    print(f'best score was {bestScore}')
    return bestMove

def playGame():
    for x in range(1):
        piece = 0
        cleared = 0
        game = Game()
        if linux:
            stdscr = curses.initscr()
        while game.running:
            for result in moveOrder(bestMove(copy.deepcopy(game.board),game.piece),game):
                print(result)
                if linux:
                    printBoard(game.train(result),stdscr)
                else:
                    #print('executing move')
                    game.train(result)
                    #print('----------')
            cleared = game.cleared
            print(game.drawBoard(prin=True))
            piece += 1
        if linux:
            curses.endwin()
        score = game.score
        print('Got a score of {:.2f}'.format(score))
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