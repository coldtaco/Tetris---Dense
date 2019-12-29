import gym
import gym_tetris
env = gym.make('Tetris-v0')
env.reset()
env.board[19][5] = 2
env.render()
print("################")
env.sp(4)
env.sr(1)
env.sm([17,5])
env.st(3)
print(env.orientation())
print(env.piece,env.rotation,env.marker)
env.move(5)
env.render()
env.move(2)
env.render()