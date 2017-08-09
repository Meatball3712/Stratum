# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import math
import numpy as np
from renderHeightmap import RenderHeightmap

class TerraGenesisInt:
    
    def __init__(self, numVecs=400, seed=0, featureScale = 256*16, minScale = 12, minScaleJump = 8):
        np.random.seed(seed)
        #generate sinusoid angles
        angles = np.random.random(size=numVecs) * math.pi
        self.dotVals = []
        for i in range(numVecs):
            pair = [np.sin(angles[i]),np.cos(angles[i])]
            scale = np.random.normal()*featureScale / np.random.choice(pair)
            self.dotVals.append(np.array(pair)*scale)
        print(self.dotVals)
        self.dotVals = np.array(self.dotVals).astype(np.int64)
        self.divVals = np.random.randint((minScale), 
                                            (minScale + minScaleJump), 
                                            size=numVecs, dtype=np.int64
                                            )
        self.offsetVals = np.random.randint(0,2**(minScale + minScaleJump),size=numVecs)
        self.heightVals = np.abs(np.random.normal(size=numVecs))
        self.heightVals /= np.sum(self.heightVals)
        
    def height(self, position):
        vals = np.abs(np.dot(self.dotVals, np.array(position,dtype=np.int64).reshape((-1,2)).T).T + self.offsetVals)
        height = np.dot(self.heightVals,  (vals >> self.divVals).T % 2 )
        return height

class TerraGenesis:
    
    def __init__(self, numVecs=500, seed=0, randScale = 5, featureScale = 5, minScale = 2, minScaleJump = 4):
        np.random.seed(seed)
        self.dotVals = np.random.normal(scale=randScale*featureScale, size=2*numVecs).reshape((-1,2))
        self.divVals = np.random.randint(minScale, 
                                            minScale + minScaleJump + int(np.log2(randScale*featureScale)), 
                                            size=numVecs)
        self.heightVals = np.abs(np.random.normal(size=numVecs))
        self.heightVals /= np.sum(self.heightVals)
        
    def height(self, position):
        vals = np.dot(self.dotVals, np.array(position).reshape((2,-1))) / self.divVals.reshape((-1,1))
        return np.dot(self.heightVals, np.sin(vals))+0.5

if __name__ == '__main__':
    img = []

    t = TerraGenesisInt()
    for i in range(1000):
        if i%100==0: print("%d%% complete" % (i/1000.0*100))
        img.append(t.height([[i,j] for j in range(1000)]))
    print(np.array(img))
    R = RenderHeightmap()
    R.output="terraGenesis.png"
    R.fromNPArray(np.array(img))