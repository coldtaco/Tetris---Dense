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
        #_max = pd.DataFrmae(self.output).sum().idxmax()
        df = pd.DataFrame(self.output)
        rand = random.randint(0,7)
        for o in range(len(self.output)):
            if random.choice(range(self.mChance)) == 0:
                temp = [0,0,0,0,0,0,0,0]
                temp[rand]=1
                self.output[o]=temp
                
    def evolve(self):
        self.mutate()
        self.create()
        
    def create(self):
        earlyStop = keras.callbacks.EarlyStopping(monitor='loss', min_delta=0.001, patience=9, verbose=0, mode='auto', baseline=None, restore_best_weights=False)
        rlr = keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.2,patience=7, min_lr=1e-6, mode='auto', verbose=1)
        self.base.fit(np.array(self.intake,dtype='float32'),np.array(self.output,dtype='float32'),validation_split=0.10, epochs=1000, batch_size=self.batch, verbose=2,callbacks=[earlyStop,rlr])
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

    def addScore(self,score):
        self.score+=score

    def addName(self,name):
        if self.name == None:
            self.name = name
    def reset(self):
        self.score = 0

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
        inputs1 = open('saves/inputs1.txt','w')
        outputs1 = open('saves/outputs1.txt','w')
        inputs2 = open('saves/inputs2.txt','w')
        outputs2 = open('saves/outputs2.txt','w')
        names = open('saves/names.txt','w')
        inputs1.write(str(self.p1.intake))
        outputs1.write(str(self.p1.output))
        inputs2.write(str(self.p2.intake))
        outputs2.write(str(self.p2.output))
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
        shuffled = list(zip(self.p1.intake,self.p1.output))
        random.shuffle(shuffled)
        intake,output = list(zip(*shuffled[:len(shuffled)*3//4]))
        shuffled = list(zip(self.p2.intake,self.p2.output))
        random.shuffle(shuffled)
        ti,to = list(zip(*shuffled[:len(shuffled)*3//4]))
        intake += ti
        output += to
        child = Species(self.base,list(intake),list(output),self.mChance)
        return child

    def findBest(self):
        bestScore = self.population[0].score
        index = 0
        for i,m in enumerate(self.population):
            if m.score > bestScore:
                bestScore = m.score
                index = i
        self.p1 = self.population.pop(index)
        bestScore = self.population[0].score
        index1 = 0
        for i,m in enumerate(self.population):
            if m.score > bestScore:
                bestScore = m.score
                index1 = i
        self.p2 = self.population[index1]
        self.population.append(self.p1)

