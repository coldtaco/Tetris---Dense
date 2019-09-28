from selenium import webdriver
import numpy
from keras import layers
import tensorflow as tf
import random
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
    model.add(Dense(8,activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

def initializeModels():
    model = newModel()
    generations = Generation(model,mChance)
    for i in range(2):
        board = [0 for x in range(10)]
        board = [list(board) for x in range(20)]
        species = Species(model,[board]*2,[[1,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,0]],mChance)
        species.evolve()
        species.addName('Gen 0, Species {}'.format(i))
        print(species.name)
        playGame(species)
        generations.population.append(species)
        print('For a total of {:.2f}!'.format(species.score))
    generations.breed()
    generations.child.addName('Gen 0, Species Child')
    generations.saveGen()
    print('Finished initialization!')
    return generations

def printBoard(board,stdscr):
    for i,l in enumerate(board):
        stdscr.addstr(i,0,l)
    stdscr.refresh()

def playGame(species):
    for x in range(10):
        if linux:
            game = Game()
            stdscr = curses.initscr()
            while game.running:
                board = game.board
                result = species.predict(board)
                game.train(result)
                printBoard(game.train(result),stdscr)
            score = game.score
            species.addScores(game)
            curses.endwin()
        else:
            game = Game()
            while game.running:
                board = game.board
                result = species.predict(board)
                game.play(result)
            score = game.score
            species.addScores(game)
        print('Got a score of {:.2f}'.format(score))

mChance = 3
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.Session(config=config)
try:
    genFile = open('gen.txt','r')
    read = genFile.readlines()
    totalGen = int(read[0])+1
    genFile.close()
except:
    totalGen=0

try:
    inputs1 = np.load('saves/inputs1.npy').tolist()
    outputs1 = np.load('saves/outputs1.npy').tolist()
    inputs2 = np.load('saves/inputs2.npy').tolist()
    outputs2 = np.load('saves/outputs2.npy').tolist()
    modelp1 = load_model('saves/p1.h5')
    modelp2 = load_model('saves/p2.h5')
    names = open('saves/names.txt').readlines()
    generations = Generation(modelp1,mChance)
    generations.p1=Species(modelp1,inputs1,outputs1,mChance)
    generations.p2=Species(modelp2,inputs2,outputs2,mChance)
    generations.p1.addName(names[0])
    generations.p2.addName(names[1])
    generations.breed()
    generations.child.addName('Gen {}, Species Child'.format(totalGen))
    print('Load models successful!')
    print('Continuing at Gen {}'.format(totalGen))
except Exception:
    totalGen=0
    traceback.print_exc()
    print("Couldn't find save files... Initializing models")
    generations = initializeModels()
            
def reset():
    try:
        intake = np.load('saves/DInput.npy',dtype='float32')
        output = np.load('saves/DOutput.npy',dtype='float32')
        intake = np.vstack([intake,lastGen.p1.intake,lastGen.p2.intake])
        output = np.vstack([intake,lastGen.p1.output,lastGen.p2.output])
    except:
        traceback.print_exc()
        intake = np.vstack([lastGen.p1.intake,lastGen.p2.intake])
        output = np.vstack([lastGen.p1.output,lastGen.p2.output])
    p = np.random.permutation(output.shape[0])
    intake,output = intake[p],output[p]
    if output.shape[0] > 1500000:
        intake,output = intake[:1500000], output[:1500000]
    np.save("saves/DInput.npy",intake)
    np.save("saves/DOutput.npy",output)
    tempSpecies = Species(newModel(),intake,output,mChance)
    tempSpecies.create()
    gen = Generation(tempSpecies.base,mChance)
    return gen

for i in range(100):
    lastGen = generations
    txt = open('tetris.log','a')
    if (i + totalGen) % 10 == 0:
        gen = reset()
        lastGen.p1.intake,lastGen.p1.output,lastGen.p2.intake,lastGen.p2.output = [],[],[],[]
    else:
        gen = Generation(lastGen.base,mChance)
    gen.population.append(lastGen.child)
    gen.population[0].addName('Gen {}, Species {}'.format(i+totalGen,'Child'))
    gen.population.append(lastGen.p1)
    gen.population.append(lastGen.p2)
    for j in gen.population:
        j.reset()
        print(" ")
        print(j.name)
        playGame(j)
        print('For a total of {:.2f}!'.format(j.score))
    for j in range(5):
        species = lastGen.createChild()
        species.evolve()
        print(" ")
        species.addName('Gen {}, Species {}'.format(i+totalGen,j))
        print(species.name)
        playGame(species)
        print('For a total of {:.2f}!'.format(species.score))
        gen.population.append(species)
        txt.write('{}, {}, finished with a score of {:.2f}, clearing {} lines\n'.format(strftime("%d %b %Y %H:%M:%S", localtime()),species.name,species.score,species.cleared))
    gen.breed()
    gen.saveGen()
    if (i + totalGen) % 10 == 0:
        print('Saving best models...')
        gen.p1.base.save('Models/Gen{}_p1.h5'.format(i+totalGen))
        gen.p2.base.save('Models/Gen{}_p2.h5'.format(i+totalGen))
    generations = gen
    genFile = open('gen.txt','w')
    genFile.write(str(totalGen+i))
    genFile.close()

