'''
Created on Sep 19, 2012

@author: ego
'''

from data.processData import processData
from som.somModule import somModule
from data.inputData import inputData
from collections import defaultdict
#import sys


class lamstar(object):
    '''
    classdocs
    '''
    def __init__(self, noOfInputs, noOfOutputs):
        '''
        Constructor
        '''
        self.debug = 1
        self.noOfInputs = noOfInputs
        self.noOfOutputs = noOfOutputs
        self.inputSOMs = []
        self.outputSOMs = []
        for _ in range(noOfInputs):
            self.inputSOMs.append(somModule(1))
        for _ in range(noOfOutputs):
            self.outputSOMs.append(somModule(1))

        self.Link2OutputDict = {}
        self.Link2LinkDict = {}

    def train(self, inputs, outputs):
        '''
        In BMU we store in form of list of tuples, the link between BMU
        in the respective SOM and the respective output
        So finally BMU is a triple (somModuleNumber,BMU,output)
        '''
#        prevNode = None
        for i in range(self.noOfInputs):
            if(self.debug > 1):
                print('Training inPat = %s outPat = %s' % (inputs[i], outputs))
            nextNode = self.inputSOMs[i].train(inputs[i])
            self.reward((i, nextNode, outputs))

#            prevNode = nextNode
#        if self.debug > 0:
#            print('Links2Output = %s' %str(self.Link2OutputDict))
#            raw_input('Enter')

#        self.forget()

    def reward(self, key):
        if self.Link2OutputDict.has_key(key):
            self.Link2OutputDict[key] += 1
        else:
            self.Link2OutputDict[key] = 1

    def forget(self):
        for key in self.Link2OutputDict.keys():
            self.Link2OutputDict[key] *= 0.99

    def goToSleep(self):
        '''
        Here we perform tasks that compact and optimize the database ...
        The Algorithm goes to sleep for regeneration :)
        '''
        self.hashTable = {}
        for key in self.LinkTable.keys():
            print (key, key[0])
            self.hashTable.setdefault(key[0], []).append(key)

    def query(self, inputs):
        '''
        Here BMU is just a list of tuples(2 values) that hold the pair
        (somModule,BMU(best somNode in somModule)).
        '''

        BMU = []
        for i in range(self.noOfInputs):
            idx = self.inputSOMs[i].query(inputs[i], self.Link2OutputDict, i)
            BMU.append((i, idx))
        if self.debug > 0:
            print('[(somModule,somNode) ...]')
            print('BMU = %s' % BMU)
        db = defaultdict(list)
        for ahash in BMU:
            for key in self.Link2OutputDict.keys():
                if key[0:2] == ahash:
                    db[key[-1]].append(self.Link2OutputDict[key])
                    print 'key=%s db[key[-1]=%s' % (key, db[key[-1]])

        if self.debug > 0:
            print('Scores:')
            for key in db.keys():
                print('%s = %s' % (key, str(sum(db[key]))))
        print('Result is:')
        print(self.maxFromDict(db))
#        raw_input('Enter')
        return (self.maxFromDict(db), BMU)

    def printSOMs(self):
        for i in range(self.noOfInputs):
            self.inputSOMs[i].printNodes()

    def getInputNode(self, i, index):
        return self.inputSOMs[i].getNodeAt(index)

    def getNoOfNodes(self):
        noNodes = 0
        best = 0
        for i in range(self.noOfInputs):
            noNodes = self.inputSOMs[i].getNoOfNodes()
            if noNodes > best:
                best = noNodes
        return noNodes

    def getNoOfLinks(self):
        return len(self.Link2OutputDict)

    def printTable(self):
        for key in sorted(self.LinkTable.keys()):
            print('%s %s' % (key, self.LinkTable[key]))

    def maxFromDict(self, dictionary):
        return max(dictionary.iteritems(), key=lambda item: sum(item[1]))[0]


if __name__ == '__main__':

    procData = processData('data/images/processed/all/150x200.pat')
    result = procData.readContents()
    data = inputData()
    data.addAll(result)

    preData = processData('data/images/processed/unseen/unseen.pat')
    result = preData.readContents()
    unseenData = inputData()
    unseenData.addAll(result)

    ls = lamstar(10, 1)
    for _ in range(10):
        for i in range(data.getCount()):
#            print('Training data : ', i)
            ls.train(data.getSubWords(i), data.getOutputs(i))
#            sys.stdin.read(1)

#    ls.printSOMs()
#    ls.printTable()

    print('\nQuering without noise:')
    for i in range(data.getCount()):
        print('\n\nQuerying for '), data.getOutputs(i)
        ls.query(data.getSubWords(i))

#    print('\nQuering with noise:')
#    for i in range(data.getCount()):
#        print('\n\nQuerying for '),data.getOutputs(i)
#        ls.query(data.getSubWordsWithNoise(i))
#Quering for unseen data:
    print('Quering for unseen data')
    for i in range(unseenData.getCount()):
        ls.query(unseenData.getSubWords(i))
