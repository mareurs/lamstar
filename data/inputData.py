'''
Created on Sep 19, 2012

@author: ego
'''
import numpy as np

class inputData(object):
    '''
        Here we deal with the generation of input words and their decomposition
        in subwords ...
    '''

    def __init__(self):
        self.data = []
    
    def addOne(self,inputValue,outputValue):              
        if not isinstance(inputValue,np.ndarray):
            raise(ValueError,'Input should belong to np.ndarray')
#        if not isinstance(outputValue,np.ndarray):
#            raise(ValueError,'Output should belong to np.ndaray')
        self.data.append((inputValue,outputValue))
        
    def addAll(self,allData):
        for inputs,outputs in allData:
            self.addOne(inputs, outputs)
        
    def getData(self,index):
        if index > len(self.data):
            raise(ValueError,'Index exceeds list''s length')
        return self.data[index]
    
    def getSubWords(self,index):
        '''
        Return the subwords decomposition of the pattern with the specified index
        The subwords are normalized [0...1] by dividing the array to the max value in the array
        '''
        '''This is the old style
        subwords = []
        for i in range(self.data[0][0].shape[0]):
            tmp = self.normalize(self.data[index][0][i,:])
            subwords.append(tmp)
            
        for i in range(self.data[0][0].shape[1]):
            tmp = self.normalize(self.data[index][0][:,i])
            subwords.append(tmp)
            
            '''
        subwords = []
        dx = 50
        dy = 40
        
        for i in range(3):
            for j in range(5):
                x = dx * i
                y = dy * j                       
#                tmp = self.normalize(self.data[index][0][x:x+dx,y:y+dy])
                tmp = self.normalize(self.data[index][0][y:y+dy,x:x+dx])

                subwords.append(tmp)           
        return subwords
    
    def getWholeArray(self,index):
        return self.data[index][0]
    
    def getSubWordsWithNoise(self,index):
        noisePercent = 0.2
        subwords = []
        for i in range(self.data[0][0].shape[0]):
            tmp = self.normalize(self.data[index][0][i,:])
            subwords.append(tmp)
        for i in range(int(len(subwords)*noisePercent/2)):
            idx1 = np.random.randint(self.data[0][0].shape[1])
            idx2 = np.random.randint(self.data[0][0].shape[1])
            subwords[idx1],subwords[idx2] = subwords[idx2],subwords[idx1]

        for i in range(self.data[0][0].shape[1]):
            tmp = self.normalize(self.data[index][0][:,i])
            subwords.append(tmp)
        for i in range(int(len(subwords)*noisePercent/2)):
            idx1 = np.random.randint(self.data[0][0].shape[0])
            idx2 = np.random.randint(self.data[0][0].shape[0])
            subwords[idx1],subwords[idx2] = subwords[idx2],subwords[idx1]
        
        return subwords
        
    def getOutputs(self,index):
        return self.data[index][1]
    
    def getCount(self):
        return len(self.data)
        
    def normalize(self,subword):
        if (subword == 0).all():
            return subword
        
        norm = subword/subword.max()
#        norm = subword/255

        return norm
        