'''
Created on Sep 18, 2012

@author: ego
'''

import pickle
import numpy as np
import os

if __name__ == '__main__':
    pass

files = ['letterA.txt','letterC.txt','letterX.txt','letterD.txt','rest1.txt','rest2.txt','rest3.txt']

for afile in files:
    if os.path.exists(afile):
        print(afile + ' exists! Removing ...')
        os.remove(afile)


letterA = np.array([(1,1,1),(1,0,1),(1,0,1)],float)
letterC = np.array([(1,1,1),(1,0,0),(1,1,1)],float)
letterX = np.array([(1,0,1),(0,1,0),(1,0,1)],float)
letterD = np.array([(1,1,1),(1,0,1),(1,1,1)],float)
rest1 = np.array([(1,1,1),(1,1,1),(1,1,1)],float)
rest2 = np.array([(0,0,0),(0,0,0),(0,0,0)],float)
rest3 = np.array([(0,1,0),(0,1,0),(0,1,0)],float)

f = open('letterA.txt','w+')
pickle.dump(letterA, f)
f.close()

f = open('letterC.txt','w+')
pickle.dump(letterC, f)
f.close()

f = open('letterX.txt','w+')
pickle.dump(letterX, f)
f.close()

f = open('letterD.txt','w+')
pickle.dump(letterD, f)
f.close()
f = open('rest1.txt','w+')
pickle.dump(rest1, f)
f.close()
f = open('rest2.txt','w+')
pickle.dump(rest2, f)
f.close()
f = open('rest3.txt','w+')
pickle.dump(rest3, f)
f.close()

