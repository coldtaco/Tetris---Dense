import numpy
from keras import layers
import tensorflow as tf
import numpy as np
from keras.models import Sequential, load_model
from keras.layers import Activation, Dense, Flatten, Reshape, LSTM
from keras import losses
import matplotlib.pyplot as plt
from species import Species, Generation
from time import localtime, strftime
import traceback
from tetris import Game
import sys
import scoring
from keras.metrics import categorical_accuracy
from tetrisFunctions import printBoard, getScore

linux = False
if sys.platform == "linux" or sys.platform == "linux2":
    import curses
    linux = True
    pass

def newModel():
    model = Sequential()
    model.add(Dense(200,activation='sigmoid',input_shape=(20,10)))
    model.add(Dense(1800,activation='softplus'))
    model.add(Dense(1800,activation='softplus'))
    model.add(Dense(1800,activation='softplus'))
    model.add(Dense(600,activation='softplus'))
    model.add(Dense(200,activation='softplus'))
    model.add(Flatten())
    model.add(Dense(200,activation='softmax'))
    model.add(Dense(8,activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

def initializeModels():
    model = newModel()
    board = [0 for x in range(10)]
    board = [list(board) for x in range(20)]
    species = Species(model,[board]*2,[[1,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,0]],0)
    assert (len(species.intake) == len(species.output))
    species.create()
    return species
    
def playGame(species):
    for x in range(10):
        t = []
        piece = 0
        cleared = 0
        game = Game()
        if linux:
            stdscr = curses.initscr()
        while game.running:
            board = game.board
            result = species.reinPred(board)
            if linux:
                printBoard(game.train(result),stdscr)
            else:
                game.play(result)
                print('##########')
            if game.pieces != piece:
                t.append(piece)
                species.reinPredNext(getScore(game, cleared))
                piece = game.pieces
                cleared = game.cleared
        if linux:
            curses.endwin()
        score = game.score
        species.addScores(game)
        print('Got a score of {:.2f}'.format(score))

#config = tf.ConfigProto()
#config.gpu_options.allow_growth = True
#session = tf.Session(config=config)
#not needed for tensorflow 2
mChance = 0
try:
    genFile = open('gen.txt','r')
    read = genFile.readlines()
    totalGen = int(read[0])+1
    genFile.close()
except:
    totalGen=0

try:
    inputs1 = np.load('saves/inputsr.npy').tolist()
    outputs1 = np.load('saves/outputsr.npy').tolist()
    modelp1 = load_model('saves/pr.h5')
    species = Species(modelp1,inputs1,outputs1,mChance)
    print('Load models successful!')
except Exception:
    totalGen=0
    traceback.print_exc()
    print("Couldn't find save files... Initializing models")
    species = initializeModels()

for i in range(100):
    if i%10 == 0:
        species.save(f'pr{i}.h5')
    playGame(species)
    print(f'For a total of {species.score:.2f}!')
    species.create()
    species.output = []
    species.intake = []
    with open('tetris.log','a') as log:
        log.write(f'{strftime("%d %b %Y %H:%M:%S", localtime())}, {species.name}, finished with a score of {species.score:.2f}, clearing {species.cleared} lines\n')
    with open('gen.txt','w') as genFile:
        genFile.write(str(totalGen+i))