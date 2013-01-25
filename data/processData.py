'''
Created on Sep 21, 2012

@author: ego
'''
import numpy as np

class processData(object):
    '''
    processData reads the contents of a .pat file with the stored data set and:
     - brakes it in input/output pairs
     
     Eventually it should be merged with inputData and injectData
    '''


    def __init__(self,filename):
        '''
        The __init__ takes as parameter the .pat file where the dataset is stored
        '''
        self.debug = 1
        self.filename = filename
        self.inputs = []
        self.outputs= []
 
        try:
            self.f = open(self.filename,'r')
        except IOError:
            print('Error opening the file %s' %self.filename)
#            self.f.close()
            exit(1)
            
    def readContents(self):
        line = self.f.readline() 
        while(line):
            if(line.find('input') > 0):
                self.noOfInputs = line[-2:]
            elif(line.find('output')>0):
                self.noOfOutputs = line[-2:]
            elif(line.find('Input') > 0):
                line = self.extractOneSample()
                continue
            line = self.f.readline()
        
        self.result = zip(self.inputs,self.outputs)
        if self.debug > 0:
            print('Printing the zipped Input/Output patterns')
        self.f.close()
        return self.result
   
   
    def extractOneSample(self):
        '''
        Read from the file untill the next line containing 'Input' is reached(meaning next pattern) 
        or reaching EOF
        '''
        inputData = ''
        outputData = ''
        line = self.f.readline()
        while(line.find('Output') < 0):
            inputData+=line[:-1]
            line = self.f.readline()
        arr = np.fromstring(inputData,sep=' ')
        #Here the reshape should be automatic !!! How?!?(aprox. square)
        self.inputs.append(arr.reshape(200,150))

        while(line.find('Input') < 0):
            outputData = self.f.readline()[:-1]
            self.outputs.append(outputData)
            line = self.f.readline()
            if not line:
                break
        return line 
    
if __name__ == '__main__':
            
    data = processData()
    data.readContents()
        