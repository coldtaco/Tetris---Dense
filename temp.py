from tetris import Game
import scoring
import numpy as np

x = Game()
board = x.board
for y in range(len(board)):
    if y > 16:
        board[y][0] = 2
        board[y][2] = 2
        board[y][3] = 2
print(board)
print(scoring.distance(board))