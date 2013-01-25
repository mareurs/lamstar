import numpy as np
from scipy.misc.pilutil import imread

imread

'''from PIL import Image

np.set_printoptions(threshold='nan')
def PIL2array(img):
    return np.array(img.getdata()).reshape(img.size[1],img.size[0])

def main():
    img  = Image.open('me1.jpg')
#    img.resize((400,300))
    print img.mode
    arr = PIL2array(img)
    print(arr)

if __name__ == '__main__':
    main()
'''
np.set_printoptions(threshold='nan')
def img2array(afilename):
    img = imread(afilename,0)
#    return np.array(img)
    return img