'''
Created on Sep 18, 2012

@author: ego
'''

import numpy as np
import random


class somNode(object):

    '''
        An universal SOM node class
    '''
    def __init__(self):
        self.iTimesModified = 0

    def setNodeProperties(self, shape):
        self.shape = shape
        self.weights = np.random.random_sample(shape)

    def getWeights(self):
        return self.weights

    def setPosition(self, position):
        if not isinstance(position, tuple) and len(position) != 2:
            raise (ValueError, 'Position is not a tuple')
        self.position = position

    def getPosition(self):
        return self.position

    def setWeights(self, data):
        self.weights = data


class somModule(object):
    '''
        the class defines somNodes and opperations on them ...
    '''

    def __init__(self, gridDimension, shape=None, gridXYvalues=None):
        '''
            The constructor of the somModule. Can take as parameter
            the shape of the SOM module or default it to None for dynamic size
            gridDimension defines the dimension of the SOM module
            if gridDimension = 2 (2d), 1(1d)
        '''
        self.debug = 2
        self.radius = 0
        self.noOfTrains = 0
        self.trainSeq = 0

        if(shape is not None):
            self.shape = shape
            self.type = 'static'
        self.nodes = []

        if gridDimension == 1:
            self.grid = None
        else:
            self.grid = gridXYvalues
        np.set_printoptions(precision=3, threshold=100)

    def setShape(self, shape, atype):
        self.shape = shape
        self.type = atype

    def addNode(self, node, position=None):
        if not isinstance(node, somNode):
            raise (ValueError, 'node is not of type somNode')
        #Some verification here about the validity of position
        self.nodes.append(node)

    def addRandomNode(self, index, shape):
        randNode = somNode()
        randNode.setNodeProperties(shape)
        self.nodes.insert(index, randNode)

    def addDefaultNode(self, example):
        defNode = somNode()
        defNode.setNodeProperties(example.shape)
        defNode.setWeights(example)
        self.nodes.append(defNode)

    def addStaticNodes(self, shape):
        for i in range(50):
            self.nodes.append(somNode())
            self.nodes[i].setNodeProperties(shape)

    def printNodes(self):
        for i in range(len(self.nodes)):
            print('Node '), i
            print(self.nodes[i].getWeights())

    def getNodeAt(self, index):
        return self.nodes[index].getWeights()

    def findBMU(self, data):
        best = 100000
        norm = 0
        bestIndex = 0
        for i in range(len(self.nodes)):
            norm = self.calculateDistance(self.nodes[i].getWeights(), data)
#            if self.debug > 1:
#                print('norm = ', norm)
            if norm < best:
                best = norm
                bestIndex = i
#            norm = 0
        if self.debug > 2:
            print('Input node is: %s' % (data))
            print('Best node is: ' + str(self.nodes[bestIndex].getWeights()) + '\nBest distance is: ' + str(best))
        if self.debug > 2:
            print('Best distance is: ', best)
        return (bestIndex, best)

    def findSmallBMU(self, data):
        best = 100000
        norm = 0
        bestIndex = 0
        for i in range(len(self.nodes)):
            norm = self.calculateDistance(self.nodes[i].getWeights()[5:-5, 5:-5], data)
#            if self.debug > 2:
#                print('norm = ', norm)
            if norm < best:
                best = norm
                bestIndex = i
        return (bestIndex, best)

    def calculateDistance(self, data1, data2):
        if self.debug > 2:
            print('Data 1' + str(data1))
            print('Data 2' + str(data2))
        if data1.shape != data2.shape:
            raise (ValueError, 'data1 and data2 have different shapes')

        distance = ((data1 - data2) ** 2).sum()
        return np.sqrt(distance) / 15
        ##(data1.shape[0]*data1.shape[1])

    def train(self, example):
        self.trainSeq += 1
        if len(self.nodes) == 0:
#            self.addStaticNodes(example.shape)
#            self.addDefaultNode(example)

            self.addRandomNode(0, example.shape)
            self.train1neuron(0, example)
            if self.debug > 0:
                print('Creating first node:')
            if self.debug > 1:
                print(self.nodes[0].getWeights())
#                raw_input("Enter")
            return 0

        (index, bestDistance) = self.findBMU(example)
        if(bestDistance > 0.3):
            #Randomize where to put the new node so they
            #don't all go on the same side
            ans = random.choice([True, False])
            if ans:
                index += 1
            else:
                index -= 1
            if index == -1:
                index = 1
            elif index == len(self.nodes) - 1:
                index = len(self.nodes) - 2

            self.addRandomNode(index, example.shape)
            self.train1neuron(index, example)
            if self.debug > 0:
                print('Added default node:')
                d = self.calculateDistance(self.nodes[index].getWeights(), example)
                print('Distance: %s' % d)
                if d > 2:
                    print self.nodes[index].getWeights()
                    print example
                    raw_input('Oooops')
            if self.debug > 2:
                print(self.nodes[index].getWeights())
                print self.nodes[index].iTimesModified
                raw_input("Enter")
            return len(self.nodes) - 1
        else:
            self.train1neuron(index, example)
            if self.debug > 2:
                print('Best node is:')
                print(self.nodes[index].getWeights())
            if self.debug > 4:
                if(self.nodes[index].iTimesModified > 1):
                    print 'iTimesModified=', self.nodes[index].iTimesModified
#                    raw_input("Enter")
            return index

    def query(self, example, linkTable, idx):
        y = example.shape[0]
        x = example.shape[1]
#        for i in range(10):
#        (index,_) = self.findBMU(example)
#          self.train1neuron(index, example,'query')
#        return index
        bestVal = 20
        aClass = 'none'
        for i in range(10):
            for j in range(10):
                (index, val) = self.findSmallBMU(example[i:y - 10 + i, j:x - 10 + j])
                if self.debug > 10:
                    for key in linkTable.keys():
                        if key[0:2] == (idx, index):
                            aClass = key[-1]
                    print('index:%s val:%s class:%s' % (index, val, aClass))

                if(val < bestVal):
                    bestVal = val
                    bestIndex = index
        if self.debug > 2:
            for key in linkTable.keys():
                if key[0:2] == (idx, bestIndex):
                    aClass = key[-1]
            print('Best index=%s ; Best value=%s Class=%s' % (bestIndex, bestVal, aClass))
#            raw_input('Enter')
        self.train1neuron(bestIndex, example, 'query')
        return bestIndex

    def train1neuron(self, index, example, where='train'):
        self.nodes[index].iTimesModified += 1
        self.noOfTrains += 1
#        learningRate = 1 * np.exp(-float(self.noOfTrains)/1000)
        self.radius = int(len(self.nodes) * np.exp(-float(self.trainSeq) / 10))
        if self.radius % 2 == 0:
            self.radius += 1

        for i in range(self.radius):
            tmpidx = index - self.radius / 2 + i
            learningRate = 1 * (np.exp(-float(self.nodes[index].iTimesModified) / 10))
            if tmpidx < 0 or tmpidx > len(self.nodes) - 1:
                continue
            proximity = np.exp(-float(np.abs(self.radius / 2 - i)) / (self.radius * 2))
            self.nodes[tmpidx].setWeights(self.nodes[tmpidx].getWeights() + \
                 proximity * learningRate * (example - self.nodes[tmpidx].getWeights()))
#        where = 'query'
        if self.debug > 0 and (where == 'query' or ((where == 'train') and (self.noOfTrains % 100 == 0))):
            print ('nodes=%s rad=%s lern=%s index=%s' % (len(self.nodes), self.radius, learningRate, index))
            print ('dx = %s' % self.calculateDistance(self.nodes[index].getWeights(), example))
#            raw_input('Enter')

        #self.nodes[index].setWeights(example)
    def getNoOfNodes(self):
        return len(self.nodes)
