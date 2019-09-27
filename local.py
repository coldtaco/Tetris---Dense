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
            species.addScore(score)
            curses.endwin()
        else:
            game = Game()
            while game.running:
                board = game.board
                result = species.predict(board)
                game.play(result)
            score = game.score
            species.addScore(score)
        print('Got a score of {:.2f}'.format(score))

mChance = 3
try:
    genFile = open('gen.txt','r')
    read = genFile.readlines()
    totalGen = int(read[0])+1
    genFile.close()
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    session = tf.Session(config=config)
except:
    totalGen=1
try:
    inputs1 = eval(open('saves/inputs1.txt','r').readlines()[0])
    outputs1 = eval(open('saves/outputs1.txt','r').readlines()[0])
    inputs2 = eval(open('saves/inputs2.txt','r').readlines()[0])
    outputs2 = eval(open('saves/outputs2.txt','r').readlines()[0])
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
    traceback.print_exc()
    print("Couldn't find save files... Initializing models")
    generations = initializeModels()

for i in range(100):
    lastGen = generations
    txt = open('tetris.log','a')
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
        txt.write('{}, {}, finished with a score of {:.2f}\n'.format(strftime("%d %b %Y %H:%M:%S", localtime()),species.name,species.score))
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

