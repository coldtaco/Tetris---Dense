import random
import numpy as np
import pandas as pd
import keras
txt = open('inputs.py','w')
class Species:
    def __init__(self,base,intake,output,mChance):
        self.base = base
        self.intake = intake
        self.output = output
        self.mChance = mChance
        self.score = 0
        self.name = None
        self.batch = self.batchSize()
        self.cleared = 0
        self.hiddenScore = 0
        self.reinTempList = []
        self.decay = 0.7

    def batchSize(self):
        length = len(self.output)
        if length > 10240:
            return 1024
        elif length > 5120:
            return 512
        elif length > 2560:
            return 256
        elif length > 1280:
            return 128
        elif length > 640:
            return 640
        elif length > 320:
            return 32
        return 16

    def mutate(self):
        if not isinstance(self.intake,np.ndarray):
            self.intake = np.array(self.intake,dtype='int8')
        if not isinstance(self.output,np.ndarray):
            self.output = np.array(self.output,dtype='float32')
        #_max = pd.DataFrmae(self.output).sum().idxmax()
        df = pd.DataFrame(self.output)
        rand = random.randint(0,7)
        p = np.random.choice(self.output.shape[0],self.output.shape[0]//self.mChance,replace=False)
        temp = [0,0,0,0,0,0,0,0]
        temp[rand]=1
        self.output[p] = np.array(temp)
                
    def evolve(self):
        self.mutate()
        self.create()
        
    def create(self):
        earlyStop = keras.callbacks.EarlyStopping(monitor='loss', min_delta=0.001, patience=9, verbose=0, mode='min', baseline=None, restore_best_weights=False)
        rlr = keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.2,patience=7, min_lr=1e-6, mode='auto', verbose=1)
        self.base.fit(np.array(self.intake,dtype='float32'),np.array(self.output,dtype='float32'),validation_split=0.10, epochs=1000, batch_size=self.batch, verbose=2,callbacks=[earlyStop,rlr])
        if isinstance(self.intake,np.ndarray):
            self.intake = self.intake.tolist()
        if isinstance(self.output,np.ndarray):
            self.output = self.output.tolist()
        return 
        
    def predict(self,intake):
        self.intake.append(intake)
        predict = self.base.predict(np.array([intake]))
        if random.choice(range(self.mChance)) == 0:
            rand = random.randint(0,7)
            temp = [0,0,0,0,0,0,0,0]
            temp[rand]=1
            self.output.append(temp)
            return rand
        self.output.append(predict.tolist()[0])
        return np.argmax(predict)

    def addScores(self,game):
        self.cleared += game.cleared
        self.score += game.score
        self.hiddenScore += game.hiddenScore

    def addName(self,name):
        if self.name == None:
            self.name = name

    def reset(self):
        self.score = 0

    def reinPred(self,intake):
        self.intake.append(intake)
        predict = self.base.predict(np.array([intake]))
        if self.mChance > 0:
            if random.choice(range(self.mChance)) == 0:
                rand = random.randint(0,7)
                self.reinTempList.append(rand)
                return rand
        self.reinTempList.append(np.argmax(predict))
        return np.argmax(predict)

    def reinPredNext(self,score):
        length = len(self.reinTempList)
        for i,x in enumerate(self.reinTempList):
            lst = [0,0,0,0,0,0,0,0]
            lst[x] = score*(self.decay**(length - i))
            self.output.append(lst)
        self.reinTempList = []

    def save(self, name): #used to save reinforcement learning model
        print('Backing up...')
        np.save('saves/inputsr',np.array(self.intake))
        np.save('saves/outputsr',np.array(self.output))
        self.base.save('saves/pr.h5')

class Generation:
    def __init__(self,base,mChance):
        self.base = base
        self.population = []
        self.mChance = mChance
        self.p1 = None
        self.p2 = None
        self.child = None

    def saveGen(self):
        print('Backing up...')
        names = open('saves/names.txt','w')
        np.save('saves/inputs1',np.array(self.p1.intake))
        np.save('saves/inputs2',np.array(self.p2.intake))
        np.save('saves/outputs1',np.array(self.p1.output))
        np.save('saves/outputs2',np.array(self.p2.output))
        names.write(self.p1.name+"\n")
        names.write(self.p2.name)
        self.p1.base.save('saves/p1.h5')
        self.p2.base.save('saves/p2.h5')

    def breed(self):
        child = self.createChild()
        child.create()
        self.child = child
    
    def createChild(self):
        if self.p1 == None or self.p2 == None:
            self.findBest()
        intake = np.vstack([self.p1.intake,self.p2.intake])
        output = np.vstack([self.p1.output,self.p2.output])
        p = np.random.permutation(output.shape[0])
        intake,output = intake[p],output[p]
        intake,output = intake[:output.shape[0]*3//4],output[:output.shape[0]*3//4]
        child = Species(self.base,list(intake),list(output),self.mChance)
        return child

    def bestScore(self,population):
        bestScore = population[0].hiddenScore
        index = 0
        for i,m in enumerate(population):
            if m.hiddenScore > bestScore:
                bestScore = m.hiddenScore
                index = i
        return population.pop(index)
        

    def findBest(self):
        bestClear = self.population[0].cleared
        match = [self.population[0]]
        for x in self.population:
            if x.cleared == bestClear:
                match.append(x)
            elif x.cleared > bestClear:
                match = [x]
        self.p1 = self.bestScore(match)
        for i,s in enumerate(self.population):
            if s.name == self.p1.name:
                self.population.pop(i)
        bestClear = self.population[0].cleared
        match = []
        for x in self.population:
            if x.cleared == bestClear:
                match.append(x)
        self.p2 = self.bestScore(match)
        self.population.append(self.p1)