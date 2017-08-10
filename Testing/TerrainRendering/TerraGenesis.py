# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import math
import numpy as np
from renderHeightmap import RenderHeightmap

class TerraGenesisInt:
    
    noiseScale = 5.
    
    def __init__(self, numVecs=300, seed=0, featureScale = 256*8, minScale = 12, minScaleJump = 8):
        np.random.seed(seed)
        #generate sinusoid angles
        angles = np.random.random(size=numVecs) * math.pi
        self.dotVals = []
        for i in range(numVecs):
            pair = [np.sin(angles[i]),np.cos(angles[i])]
            scale = np.random.normal()*featureScale / np.random.choice(pair)
            self.dotVals.append(np.array(pair)*scale)
        self.dotVals = np.array(self.dotVals).astype(np.float32)
        self.divVals = np.random.randint((minScale), 
                                            (minScale + minScaleJump), 
                                            size=numVecs, dtype=np.int64
                                            )
        self.offsetVals = np.random.randint(0,2**(minScale + minScaleJump),size=numVecs)
        self.heightVals = np.abs(np.random.normal(size=numVecs))
        self.heightVals /= np.sum(self.heightVals)/2./self.noiseScale
        
    def height(self, position):
        vals = np.abs(np.dot(self.dotVals, position.T)).T.astype(dtype=np.int64) + self.offsetVals
        height = np.dot(self.heightVals,  (vals >> self.divVals).T % 2 )
        del vals
        return np.tanh(height-self.noiseScale)*0.5 + 0.5
    
    def chunkHeight(self, x0,y0,x1,y1, stepSize = 1.):
        x,y = np.meshgrid(np.arange(x0,x1,stepSize,dtype=np.float32), np.arange(y0,y1,stepSize,dtype=np.float32), indexing='xy')
        positions = np.vstack([x.ravel(),y.ravel()]).T
        del x,y
        return self.height(positions)

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
    img = t.chunkHeight(0,0,1000,1000).reshape((1000,1000))
    R = RenderHeightmap()
    R.output="terraGenesis.png"
    R.fromNPArray(np.array(img))
