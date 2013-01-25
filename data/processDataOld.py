'''
Created on Sep 18, 2012

@author: ego
'''
import pickle;

class processData(object):
    '''
    The class deals with loading the initial parameters
    '''

    def __init__(self):
        self.loadValues()

    def loadValues(self):
        try:
            f = open('letterA.txt')
        except IOError:
            print('IO exception ')
        self.letterA = pickle.load(f)
        f.close()
        try:
            f = open('letterC.txt')
        except IOError:
            print('IO exception ')
        self.letterC = pickle.load(f)
        f.close()
        try:
            f = open('letterX.txt')
        except IOError:
            print('IO exception ')
        self.letterX = pickle.load(f)
        f.close()
        try:
            f = open('letterD.txt')
        except IOError:
            print('IO exception ')
        self.letterD = pickle.load(f)
        f.close()
        try:
            f = open('rest1.txt')
        except IOError:
            print('IO exception ')
        self.rest1 = pickle.load(f)
        f.close()
        try:
            f = open('rest2.txt')
        except IOError:
            print('IO exception ')
        self.rest2 = pickle.load(f)
        f.close()
        try:
            f = open('rest3.txt')
        except IOError:
            print('IO exception ')
        self.rest3 = pickle.load(f)
        f.close()

        
    def getA(self):
        return self.letterA
    
    def getC(self):
        return self.letterC
    
    def getX(self):
        return self.letterX
            
    def getD(self):
        return self.letterD
    def getRest1(self):
        return self.rest1
    def getRest2(self):
        return self.rest2
    def getRest3(self):
        return self.rest3
    
    
    
    