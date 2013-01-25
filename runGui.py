#!/usr/bin/env python

'''
Created on Nov 12, 2012

@author: ego
'''
import sys
from GUI.gui import Ui_MainWindow
from PyQt4 import QtGui, QtCore
from data.injectData import injectData
from data.processData import processData
from data.inputData import inputData
import Lamstar
import os
import numpy as np


class runGUI(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(runGUI, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.createConnections()
        self.trainingDir = 'data/images/ORL/ORL/'
        self.trainPat = self.trainingDir + 'ORL.pat'
        self.testingDir = 'data/images/ORL/ORL/unseen/'
        self.testPat = self.testingDir + 'unseen.pat'
        self.debug = 1

    def createConnections(self):
        self.ui.actionLoad_Training_Folder.triggered.connect(self.loadDataFiles)
        self.ui.actionLoad_Testing_Folder.triggered.connect(self.loadDataFiles)
        self.ui.actionTrain.triggered.connect(self.train)
        self.ui.actionRun_Test.triggered.connect(self.train)
        self.ui.actionPrepare_for_training.triggered.connect(self.prepareTraining)
        self.ui.actionPrepare_for_testing.triggered.connect(self.prepareTesting)

    def loadDataFiles(self):
        if self.sender() == self.ui.actionLoad_Training_Folder:
            Call = 'Training'
        else:
            Call = 'Testing'

        dialog = QtGui.QFileDialog()
        dialog.setDirectory('.')
        dialog.setFileMode(QtGui.QFileDialog.Directory)
        dialog.exec_()
        filenames = dialog.selectedFiles()

        if Call == 'Training':
            self.trainingDir = str(filenames[0])
            self.trainPat = self.trainingDir + '/' + self.trainingDir.rpartition('/')[-1] + '.pat'
        else:
            self.testingDir = str(filenames[0])
            self.testPat = self.testingDir + '/' + self.testingDir.rpartition('/')[-1] + '.pat'

    def prepareTraining(self):
        if self.trainingDir is None:
            return None
        self.log('Cleaning previous temporary data ...', 'main')
#        self.cleanDir(self.trainingDir)
        self.log('Starting training operations ...', 'main')
        directory = self.trainingDir
        outdir = directory + '/'
        self.log('Getting faces ...', 'query')
#        fd = faceDetector(outdir,outdir)
#        fd.run()
        self.log('OK', 'status')
        self.log('Saving patterns in the .pat file ...', 'query')
        injectData(self.trainPat, outdir, 'train')
        self.log('OK', 'status')

    def prepareTesting(self):
        if self.testingDir is None:
            return None
        self.log('Cleaning previous temporary data ...', 'main')
#        self.cleanDir(self.testingDir)
        self.log('Starting testing operations ...', 'main')
        directory = self.testingDir
        outdir = directory + '/'
        self.log('Getting faces ...', 'query')
#        fd = faceDetector(outdir,outdir)
#        fd.run()
        self.log('OK', 'status')
        self.log('Saving patterns in the .pat file ...', 'query')
        injectData(self.testPat, outdir, 'test')
        self.log('OK', 'status')

    def train(self):
        allSamples = goodSamples = 0.0
        self.log('Starting the real training...', 'main')
        if self.sender() == self.ui.actionTrain:
            procData = processData(self.trainPat)
            result = procData.readContents()
            data = inputData()
            data.addAll(result)
            self.ls = Lamstar.lamstar(15, 1)
            for iter in range(10):
                print('Iteration %s' % iter)
                for i in range(data.getCount()):
#                    print('Training data : ', i)
#                    self.arr2Image(data.getWholeArray(i),'input')
#                    raw_input('Enter')
                    self.ls.train(data.getSubWords(i), data.getOutputs(i))
                if(self.debug > 0):
                    self.log('Iteration no:' + str(iter), 'main')
                    self.log('No of nodes' + str(self.ls.getNoOfNodes()), 'main')

        elif self.sender() == self.ui.actionRun_Test:
            goodSamples = allSamples = 0
            procData = processData(self.testPat)
            result = procData.readContents()
            data = inputData()
            data.addAll(result)
            files = []
            for afile in os.listdir(self.testingDir):
                if afile[-3:] == 'jpg' and afile.find('procced') != -1:
                    files.append(afile)
            files.sort()
            print('Quering for test data')
            self.log('Quering for test data', 'main')
            print('number of items: %s' % (data.getCount()))
            for i in range(data.getCount()):
                self.log('Querying for ' + files[i].rpartition('/')[-1], 'query')
                print('Querying for ' + files[i].rpartition('/')[-1])
                self.arr2Image(data.getWholeArray(i), 'input')
                (result, BMU) = self.ls.query(data.getSubWords(i))
                arr = self.constructArr(BMU)
                self.arr2Image(arr, 'output')
                self.log(result, 'status')
                allSamples += 1
                if files[i].find(result + '-') != -1:
                    goodSamples += 1
                self.ui.resultLabel.setText(result)
            self.log('No of nodes: ' + str(self.ls.getNoOfNodes()), 'main')
            self.log('No of links: ' + str(self.ls.getNoOfLinks()), 'main')
            self.log('Accuracy = ' + str((float(goodSamples) / allSamples) * 100) + '%', 'main')
            print ('Good sample=%s all=%s' % (goodSamples, allSamples))

    def constructArr(self, BMU):
        dx = 50
        dy = 40
        arr = np.zeros((200, 150))

        BMU.sort()
        for (i, idx) in BMU:
            x = (i / 5) * 50
            y = (i % 5) * 40
            arr[y:y + dy, x:x + dx] = self.ls.getInputNode(i, idx) * 255
        return arr

    def arr2Image(self, arr, holder):
        from scipy.misc import imsave
        imsave('tmp.png', arr)
#        imshow(arr)
        if holder == 'input':
            self.ui.imageInputLabel.setPixmap(QtGui.QPixmap('tmp.png'))
        elif holder == 'output':
            self.ui.imageResultLabel.setPixmap(QtGui.QPixmap('tmp.png'))

#        self.ui.imageInputLabel.setPixmap
        self.ui.imageInputLabel.repaint()

    def cleanDir(self, inputDir):
        for afile in os.listdir(inputDir):
            if afile.find('procced') != -1:
                os.remove(inputDir + '/' + afile)

    def log(self, text, mode):
        if(mode == 'query'):
            self.ui.textBrowser.setAlignment(QtCore.Qt.AlignRight)
            self.ui.textBrowser.setTextColor(QtCore.Qt.black)
            self.ui.textBrowser.insertPlainText(text)
        elif(mode == 'status'):
            self.ui.textBrowser.insertPlainText('\t[ ')
            self.ui.textBrowser.setTextColor(QtCore.Qt.green)
            self.ui.textBrowser.insertPlainText(text)
            self.ui.textBrowser.setTextColor(QtCore.Qt.black)
            self.ui.textBrowser.insertPlainText(' ]\n')
        elif(mode == 'main'):
            self.ui.textBrowser.setAlignment(QtCore.Qt.AlignLeft)
            self.ui.textBrowser.setTextColor(QtCore.Qt.red)
            self.ui.textBrowser.insertPlainText(text + '\n')
        self.ui.textBrowser.repaint()
        self.repaint()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    myapp = runGUI()
    myapp.show()
    sys.exit(app.exec_())
