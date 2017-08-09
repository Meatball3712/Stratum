# Render a 2d heightmap as pretty colours

from PIL import Image
import argparse
import numpy as np

class RenderHeightmap:
    def __init__(self, **kwargs):
        self.output = kwargs.get("output", "heightMap.png")
        self.waterHeight = kwargs.get("waterHeight", 0)

    def rainbowGradient(self, value):
        # Take a value between 0 and 1, and return a nice heatmap gradient
        if value < 0.25:
            # Blue -> Cyan
            R = 0
            G = int(value/0.25*255)
            B = 255

        elif value < 0.5:
            # Cyan -> Green
            R = 0
            G = 255
            B = 255 - int((value-0.25)/0.25 * 255)

        elif value < 0.75:
            # Green -> Yellow
            R = int((value-0.5)/0.25 * 255)
            G = 255
            B = 0

        else:
            # Yellow -> Red
            R = 255
            G = 255 - int((value-0.75)/0.25 * 255)
            B = 0

        return R,G,B

    def rainbowArray(self, nparray):
        print "Creating gradient on Array", (nparray.shape[0], nparray.shape[1], 3)
        gradient = np.zeros(shape=(nparray.shape[0], nparray.shape[1], 3))
        
        # if value < 0.25
        # Blue -> Cyan
        section = nparray <= 0.25
        gradient[:,:,0] = np.where(section, 0.0, gradient[:,:,0])                                       # R =  0
        gradient[:,:,1] = np.where(section, (nparray/0.25)*255.0, gradient[:,:,1])                      # G = 0-255
        gradient[:,:,2] = np.where(section, 255.0, gradient[:,:,2])                                     # B = 255

        #if 0.25 < value <= 0.5
        # Cyan -> Green
        section = (nparray > 0.25) & (nparray <= 0.5)
        gradient[:,:,0] = np.where(section, 0.0, gradient[:,:,0])                                       # R =  0
        gradient[:,:,1] = np.where(section, 255.0, gradient[:,:,1])                                     # G = 255
        gradient[:,:,2] = np.where(section, 255.0-(((nparray-0.25)/0.25)*255.0), gradient[:,:,2])       # B = 255-0

        #if 0.5 < value <= 0.75:
        # Green -> Yellow
        section = (nparray > 0.5) & (nparray <= 0.75)
        gradient[:,:,0] = np.where(section, ((nparray-0.5)/0.25)*255.0, gradient[:,:,0])                # R =  0-255
        gradient[:,:,1] = np.where(section, 255.0, gradient[:,:,1])                                     # G = 255
        gradient[:,:,2] = np.where(section, 0.0, gradient[:,:,2])                                       # B = 0

        #if 0.75 < value <= 1
        # Yellow -> Red
        section = (nparray > 0.75)
        print section
        gradient[:,:,0] = np.where(section, 255.0, gradient[:,:,0])                                     # R =  255
        gradient[:,:,1] = np.where(section, 255.0-(((nparray-0.75)/0.25)*255.0), gradient[:,:,1])       # G = 255-0
        gradient[:,:,2] = np.where(section, 0.0, gradient[:,:,2])                                       # B = 0

        if self.waterHeight > 0:
            section = (nparray < self.waterHeight)
            gradient[:,:,0] = np.where(section, 0.0, gradient[:,:,0])
            gradient[:,:,1] = np.where(section, 0.0, gradient[:,:,1])
            gradient[:,:,2] = np.where(section, 255.0, gradient[:,:,2])

        return gradient

    def fromNPArray(self, nparray):
        g = self.rainbowArray(nparray)
        I = Image.fromarray(np.uint8(g))
        I.save(self.output, "PNG")
        print g


def testTerraGenesis():
    print "Generating Map from TerraGenesis"
    from TerraGenesis import TerraGenesisInt
    T = TerraGenesisInt()
    map = np.zeros((1000,1000))
    for x in xrange(1000):
        if ( x % 100 == 0):
            print "%d%% done" % (x / 1000.0 * 100)
        for y in xrange(1000):
            map[x,y] = T.height((x,y))
    print "Map Generated"
    R = RenderHeightmap(waterHeight = 0.6)
    R.output = "terraGenesis.png"
    R.fromNPArray(map)

def testGradient():
    testImage = np.zeros((100,100))
    testImage[10:20,:] = 0.1
    testImage[20:30,:] = 0.2
    testImage[30:40,:] = 0.3
    testImage[40:50,:] = 0.4
    testImage[50:60,:] = 0.5
    testImage[60:70,:] = 0.6
    testImage[70:80,:] = 0.7
    testImage[80:90,:] = 0.8
    testImage[90:,:] = 0.9
    
    R = RenderHeightmap(waterHeight = 0.0)
    R.output = "testGradient.png"
    R.fromNPArray(testImage)


if __name__=="__main__":
    #testGradient()
    testTerraGenesis()


