from selenium import webdriver
from PIL import Image
from io import BytesIO, StringIO
import numpy
from keras import layers
import tensorflow as tf
import random
import numpy as np
from keras.models import Sequential, load_model
from keras.layers import Activation, Dense, Flatten, Reshape, LSTM
from keras import losses
import matplotlib.pyplot as plt
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from species import Species, Generation
from time import localtime, strftime
import traceback
def getBoard(screenshot):
    size = boardDiv.size
    location = boardDiv.location
    left = location['x']+1
    top = location['y']
    right = location['x'] + size['width']-7
    bottom = location['y'] + size['height']
    img = screenshot.crop((left, top, right, bottom)).convert("L")
    return img
def checkEnd():
    chatlen = chatDiv.find_elements_by_css_selector("*")
    return len(chatlen)

def initializeModels():
    model = Sequential()
    model.add(LSTM(200,activation='sigmoid',input_shape=(10,20)))
    model.add(LSTM(1800,activation='softplus'))
    model.add(LSTM(8,activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    generations = [Generation(model,9)]
    for i in range(2):
        species = Species(model,[[[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]],[[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]],[[1,0,0,0,0,0,0,0],[1,0,0,0,0,0,0,0]],5)
        species.evolve()
        species.addName('Gen 0, Species {}'.format(i))
        print(species.name)
        playGame(species)
        generations[0].population.append(species)
        print('For a total of {:.2f}!'.format(species.score))
    generations[0].breed()
    generations[0].child.addName('Gen 0, Species Child')
    generations[0].saveGen()
    print('Finished initialization!')
    return generations


def playGame(species):
    for x in range(2):
        boardDiv.send_keys(Keys.F4)
        driver.implicitly_wait(1)
        while goDiv.value_of_css_property('display')=='block':
            continue
        while sprintInfo.value_of_css_property('display')!='none':
            img = driver.get_screenshot_as_png()
            temp = BytesIO(img)
            screenshot = Image.open(temp)
            iBoard=getBoard(screenshot).resize((10,20),Image.ANTIALIAS)
            board = np.array(iBoard)/255
            result = species.predict(board)
            boardDiv.send_keys(moves[result])
        if sprintInfo.value_of_css_property('display')=='none':
            score = float(timeDiv.text)-float(finesseDiv.text)
            print('Got a score of {:.2f}'.format(score))
            species.addScore(score)

driver = webdriver.Chrome('../chromedriver')
driver.get('C:/Users/Yuhan/Desktop/Jstris.html')
boardDiv = driver.find_element_by_id('myCanvas')
chatDiv = driver.find_element_by_id("ch1")
timeDiv = driver.find_element_by_id('clock')
resetDiv = driver.find_element_by_id('res')
finesseDiv = driver.find_element_by_id('receivedText')
goCheckDiv = driver.find_elements_by_class_name('gCapt')
sprintInfo = driver.find_element_by_id('sprintInfo')
wait = WebDriverWait(driver, 5)
element = wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='gCapt'][3]")))
goDiv = driver.find_element_by_xpath("//div[@class='gCapt'][3]")
try:
    wait.until(EC.presence_of_element_located((By.ID,"practice-ul")))
    offlinePlay = driver.find_element_by_id("practice-ul")
    wait.until(EC.element_to_be_clickable((By.ID,"practice-ul")))
    offlinePlay.click()
except:
    pass

moves = [Keys.ARROW_LEFT,Keys.ARROW_RIGHT,Keys.ARROW_UP,Keys.ARROW_DOWN," ","z","c","a"]
mChance = 7
try:
    genFile = open('gen.txt','r')
    read = genFile.readlines()
    totalGen = int(read[0])+1
    genFile.close()
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
    generations = [Generation(modelp1,mChance)]
    gen = generations[0]
    gen.p1=Species(modelp1,inputs1,outputs1,mChance)
    gen.p2=Species(modelp2,inputs2,outputs2,mChance)
    gen.p1.addName(names[0])
    gen.p2.addName(names[1])
    gen.breed()
    gen.child.addName('Gen {}, Species Child'.format(totalGen))
    print('Load models successful!')
    print('Continuing at Gen {}'.format(totalGen))
except Exception:
    traceback.print_exc()
    print("Couldn't find save files... Initializing models")
    generations = initializeModels()
            

txt = open('tetris.log','a')
for i in range(100):
    lastGen = generations[-1]
    gen = Generation(lastGen.p1.base,mChance)
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
    print('Saving best models...')
    gen.p1.base.save('Models/Gen{}_p1.h5'.format(i+totalGen))
    gen.p2.base.save('Models/Gen{}_p2.h5'.format(i+totalGen))
    generations.append(gen)
    genFile = open('gen.txt','w')
    genFile.write(str(totalGen+i))
    genFile.close()


driver.close()
