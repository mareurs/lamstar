'''
Created on Sep 25, 2012

@author: ego
'''
from datetime import date
import re
import os
#from Lamstar import imageProcessing.imageConvert
#from Lamstar.imageProcessing import imageConvert
from imageProcessing import imageConvert


class injectData(object):
    '''
    This class injects patterns into a .pat file. The constructor takes the filename 
    as a paramter.The file if exists is overwritten
    '''


    def __init__(self,filename,directory,mode):
        '''
        Constructor
        '''        
        self.directory = directory + '/'
        self.filename = filename
        self.buff = ''
        self.hasHeader = False
        self.index = 1
        files = []
    
        for afile in os.listdir(directory):
            if afile.find('.jpg') < 0 or afile.find('procced') < 0:
                continue
            files.append(afile)
        files.sort()
        for afile in files:
            aninput = imageConvert.img2array(self.directory + '/' + afile)
            #m = re.search('[0-9]+',afile)
            #if m.group(0) != '' or mode != 'test':
            [begin,end] = afile.split('-')
            self.injectData(aninput, begin)
        
    def injectHeader(self,aninput,anoutput):
        self.fd = open(self.filename,'w')
        now = date.today()
        self.buff = 'Custom pattern set\n'
        self.buff+= 'Created on ' + now.isoformat() + '\n\n\n'
        noOfUnits = aninput.shape[0]*aninput.shape[1]        
        self.buff+='No. of patterns : 99\n'
        self.buff+='No. of input units : ' + str(noOfUnits) + '\n'
        self.buff+='No. of output units : 1\n\n'
        self.hasHeader = True 
        self.fd.close()
        
        
    def injectData(self,aninput,anoutput):
        '''
        Inject input and output patterns in the file specified by the constructor.
        The input needs to be an numpy.array or at least a class that supports 
        reshape (matrix,array).The output for now can be anything (string).
        '''
        
        if not self.hasHeader: 
            self.injectHeader(aninput,anoutput)
        if self.fd.closed:
            self.fd = open(self.filename,'w+')
        
#        print(aninput)
        noOfUnits = aninput.shape[0]*aninput.shape[1]        
        
        self.buff+='# Input pattern ' + str(self.index) + ':\n'
        tmp = str(aninput.reshape(1,noOfUnits))
        tmp2 = tmp[2:-2]
#        print(tmp2)
        self.buff+=str(tmp2)+'\n'
        self.buff+='# Output pattern ' + str(self.index) + ':\n'
        self.buff+=anoutput + '\n'
        self.fd.write(self.buff)
        self.fd.close()
        self.index+=1
        
if __name__ == '__main__':

    data = injectData('unseen.pat','/home/ego/Documents/Aptana Studio 3 Workspace/Dissertation/Lamstar/data/images/processed/all')
        
