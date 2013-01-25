#!/usr/bin/env python

import os
import sys

imageFiles=['jpg','png','bmp','jpeg']

if len(sys.argv) != 2:
    print('Usage: ./batchRename [rootName]')
    sys.exit(1)
#print(sys.argv)
i = 0

for afile in os.listdir('.'):
    if not afile[-3:] in imageFiles:
        continue
    i+=1
    os.rename(afile,sys.argv[1]+ str(i) + '.'+afile[-3:])


