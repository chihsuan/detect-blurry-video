""" This is an implementation of the paper found here: http://www.cs.cmu.edu/~htong/pdf/ICME04_tong.pdf 
    Extended from https://gist.github.com/shahriman/3289170
"""
from PIL import Image
import numpy
import pywt
import sys

def detect_blurry_image(image, thresh=35, MinZero=0.05):

    if type(image) is str: 
        image = Image.open(sys.argv[1]).convert('F')
        image = numpy.asarray(image)
    
    x_cropped = image[0:(numpy.shape(image)[0]/16)*16 - 1, \
                        0:(numpy.shape(image)[1]/16)*16 - 1]

    LL1,(LH1,HL1,HH1) = pywt.dwt2(x_cropped,'haar')
    LL2,(LH2,HL2,HH2) = pywt.dwt2(LL1      ,'haar')
    LL3,(LH3,HL3,HH3) = pywt.dwt2(LL2      ,'haar')
    Emap1 = numpy.square(LH1) + numpy.square(HL1) + numpy.square(HH1)
    Emap2 = numpy.square(LH2) + numpy.square(HL2) + numpy.square(HH2)
    Emap3 = numpy.square(LH3) + numpy.square(HL3) + numpy.square(HH3)

    dimx=numpy.shape(Emap1)[0] / 8
    dimy=numpy.shape(Emap1)[1] / 8
    Emax1 = []
    vert = 1
    for j in range(0, dimx - 2):
        horz = 1;
        Emax1.append([])
        for k in range(0,dimy - 2):
            Emax1[j].append(numpy.max(numpy.max(Emap1[vert:vert+7, horz:horz+7])))
            horz = horz + 8
        vert = vert + 8

    dimx = numpy.shape(Emap2)[0] / 4
    dimy = numpy.shape(Emap2)[1] / 4
    Emax2 = []
    vert = 1
    for j in range(0,dimx - 2):
        horz = 1;
        Emax2.append([])
        for k in range(0,dimy - 2):
            Emax2[j].append(numpy.max(numpy.max(Emap2[vert:vert+3,horz:horz+3])))
            horz = horz+4
        vert=vert+4

    dimx = numpy.shape(Emap3)[0]/2
    dimy = numpy.shape(Emap3)[1]/2
    Emax3 = []
    vert=1
    for j in range(0, dimx - 2):
        horz=1;
        Emax3.append([])
        for k in range(0, dimy - 2):
            Emax3[j].append(numpy.max(numpy.max(Emap3[vert:vert+1,horz:horz+1])))
            horz = horz+2
        vert = vert+2

    N_edge = 0
    N_da = 0
    N_rg = 0
    N_brg = 0

    EdgeMap = []
    for j in range(0, dimx - 2):
        EdgeMap.append([])
        for k in range(0, dimy - 2):
            if (Emax1[j][k] > thresh) or (Emax2[j][k] > thresh) or (Emax3[j][k] > thresh):
                EdgeMap[j].append(1)
                N_edge = N_edge + 1
                rg = 0
                if (Emax1[j][k] > Emax2[j][k]) and (Emax2[j][k] > Emax3[j][k]):
                    N_da=N_da+1
                elif (Emax1[j][k] < Emax2[j][k]) and (Emax2[j][k] < Emax3[j][k]):
                    rg = 1
                    N_rg=N_rg+1
                elif (Emax2[j][k] > Emax1[j][k]) and (Emax2[j][k] > Emax3[j][k]):
                    rg = 1
                    N_rg = N_rg+1
                if rg and (Emax1[j][k] < thresh):
                    N_brg = N_brg+1
            else:
                EdgeMap[j].append(0)

    per = float(N_da) / N_edge
    BlurExtent = float(N_brg) / N_rg

    if per > MinZero:
        print 'Not blurred'
        return False
    else:
        print 'Blurred'
        return True

if __name__=='__main__':
    detect_blurry_image(sys.argv[1])
