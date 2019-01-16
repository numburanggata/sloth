from PIL import Image
from collections import defaultdict
import math
import cv2
import multiprocessing
import socket
import numpy as np

def blockproc(block, num):
    for hor in range(8):
        for ver in range(8):
            frame[hor, ver] = 255,255,255
            # print num, block[0][0]

def blockelate(frame):
    # print frame[0][0]
    piycc = {}
    mulp = []
    # frame[100:116][100:116]
    print frame[0][0]
    piycc = {}

    for pixy in range(2):
        piycc[pixy] = {}
        for pixx in range(2):
            piycc[pixy][pixx] = {}
            for py8 in range(8):
                piycc[pixy][pixx][py8] = {}
                for px8 in range(8):
                    piycc[pixy][pixx][py8][px8] = frame[(pixx*8) + 100][(pixy*8) + 100]
    mulproc1 = multiprocessing.Process(target=blockproc(piycc[0][0], 1))
    mulproc2 = multiprocessing.Process(target=blockproc(piycc[0][1], 2))
    mulproc3 = multiprocessing.Process(target=blockproc(piycc[1][0], 3))
    mulproc4 = multiprocessing.Process(target=blockproc(piycc[1][1], 4))
    mulproc1.start()
    mulproc2.start()
    mulproc3.start()
    mulproc4.start()
    for blocky in range(4):
        piycc[blocky] = {}
        for blockx in range(4):
           piycc[blocky][blockx] = {}
           mulproc = multiprocessing.Process(target=blockproc(blocky, blockx))
           mulp.append(mulproc)
           mulproc.start()
           piycc[blocky][blockx] = blockproc(blocky, blockx)

           # for py8 in range(8):
           #     piycc[pixy][pixx][py8] = {}
           #     for px8 in range(8):
           #         piycc[pixy][pixx][py8][px8] = {}
                   # frame[pixy][pixx] = 255, 255, 255
                   # print 'a'
#                    piycc[pixy][pixx][py8][px8] = toYCbCr(frame[(pixx * 8) + px8][(pixy * 8) + py8])
#             dct88y[pixy][pixx] = dct(piycc[pixy][pixx])
#             print piycc[pixy][pixx]
#            if pixx % 4 == 0 and pixx != 0:
#                ymail = blockenc(dct88y[pixy][pixx - 4], dct88y[pixy][pixx - 3], dct88y[pixy][pixx - 2], dct88y[pixy][pixx - 1])
#                 cbmail = blockenc(dct88cb[pixx][pixy], dct88cb[pixx + 1][pixy], dct88cb[pixx + 2][pixy], dct88cb[pixx + 3][pixy])
#                 crmail = blockenc(dct88cr[pixx][pixy], dct88cr[pixx + 1][pixy], dct88cr[pixx + 2][pixy], dct88cr[pixx + 3][pixy])
#                 print ymail
                #print "========================444444444========================"
            #     print cbmail
            #     print crmail

def send(mail):
    print mail

def recv(mail):
    print mail

def blockenc(block0, block1, block2, block3):
    dc = str(block0[0][0]) + 'z' + str(block1[0][0]) + 'z' + str(block2[0][0]) + 'z' + str(block3[0][0]) + 'z'
    #dcenc = denc(dc)
    #print dcenc
    ac4, encac4 = defaultdict(dict), defaultdict(dict)
    ac4[0] = str(quan(block0))
    ac4[1] = str(quan(block1))
    ac4[2] = str(quan(block2))
    ac4[3] = str(quan(block3))
    #for y in range(4):
    #    for x in range(3):
    #        encac4[y][x] = aenc(ac4[y][x])
    #mail = str(dcenc) + str(encac4)
    ac4 = ac4[0] + ac4[1] + ac4[2] + ac4[3]
    mail = str(dc) + str(ac4)
    # print mail
    return mail

def quan(block):
    ac = defaultdict(dict)
    ac[0] = (str(block[1][0]) + 'x' + str(block[0][1]) + 'x' + str(block[0][2]) + 'x' + str(block[1][1])) + 'y'
    ac[1] = (str(block[2][0]) + 'x' + str(block[3][0]) + 'x' + str(block[2][1]) + 'x' + str(block[1][2])) + 'y'
    ac[2] = (str(block[0][3]) + 'x' + str(block[0][4]) + 'x' + str(block[1][3]) + 'x' + str(block[2][2])) + 'yy'
    ac = ac[0] + ac[1] + ac[2]
    #print ac
    return ac

def toYCbCr((r, g, b)):
    y = (0.299 * r) + (0.587 * g) + (0.114 * b)
    cb = -(0.1687 * r) - (0.3313 * g) + (0.5 * b) + 128
    cr = (0.5 * r) - (0.4187 * g) - (0.0813 * b) + 128
    #print y, cb, cr
    return (y, cb, cr)

def toRGB(y, cb, cr):
    r = y + (1.402 * (cr - 128))
    g = y - (0.34414 * (cb - 128)) - (0.71414 * (cr-128))
    b = y + (1.772 * (cb - 128))
    print r, g, b
    return r, g, b

def dct(block):
    dcty = defaultdict(dict)
    for dy8 in range(8):
        for dx8 in range(8):
            sumc = 0
            for y8 in range(8):
                for x8 in range(8):
                    sumct = block[x8][y8] * math.cos(((2 * x8 + 1) * dx8 * math.pi) / 16) * math.cos(((2 * y8 + 1) * dy8 * math.pi) / 16)
                    #print "block: " + str(block[x8][y8])
                    #print "cosx: " + str(math.cos(((2 * x8 + 1) * dx8 * math.pi) / 16))
                    #print "cosy: " + str(math.cos(((2 * y8 + 1) * dy8 * math.pi) / 16))
                    #print "temp: " + str(sumct)
                    sumc = sumc + sumct
                    #print "sumtemp: " + str(sumc)
            i, j = 1, 1
            if dx8 == 0:
                i = (2 ** -0.5)
            if dy8 == 0:
                j = (2 ** -0.5)
            #print i, j
            dcty[dx8][dy8] = 0.25 * i * j * sumc
            #print "dct: " + str(dcty[dx8][dy8])
            #print "round: " + str(dcty[dx8][dy8] % 1)
            if dcty[dx8][dy8] > 0:
                if dcty[dx8][dy8] % 1 > 0.5 and dcty[dx8][dy8] % 1 < 1:
                    dcty[dx8][dy8] = int(dcty[dx8][dy8]) + 1
                if dcty[dx8][dy8] % 1 <= 0.5 and dcty[dx8][dy8] % 1 > 0:
                    dcty[dx8][dy8] = int(dcty[dx8][dy8])
            elif dcty[dx8][dy8] < 0:
                if dcty[dx8][dy8] % -1 >= -0.5 and dcty[dx8][dy8] % -1 < 0:
                    dcty[dx8][dy8] = int(dcty[dx8][dy8])
                if dcty[dx8][dy8] % -1 < -0.5 and dcty[dx8][dy8] % -1 > -1:
                    dcty[dx8][dy8] = int(dcty[dx8][dy8]) - 1
            dcty[dx8][dy8] = int(dcty[dx8][dy8])
            #print str(dx8), str(dy8), str(dcty[dx8][dy8])
    return dcty
    #idct(dcty)

def idct(block):
    dcta = defaultdict(dict)
    for y8 in range(8):
        for x8 in range(8):
            sumc = 0
            for dy8 in range(8):
                for dx8 in range(8):
                    i, j = 1, 1
                    if dx8 == 0:
                        i = (2 ** -0.5)
                    if dy8 == 0:
                        j = (2 ** -0.5)
                    sumct = i * j * block[dx8][dy8] * math.cos(((2 * x8 + 1) * dx8 * math.pi) / 16) * math.cos(((2 * y8 + 1) * dy8 * math.pi) / 16)
                    #print "block: " + str(block[x8][y8])
                    #print "cosx: " + str(math.cos(((2 * x8 + 1) * dx8 * 180) / 16))
                    #print "cosy: " + str(math.cos(((2 * y8 + 1) * dy8 * 180) / 16))
                    #print "temp: " + str(sumct)
                    sumc = sumc + sumct
                    #print "sumtemp: " + str(sumc)
            dcta[x8][y8] = 0.25 * sumc
            dcta[x8][y8] = int(dcta[x8][y8])
            print str(x8), str(y8), str(dcta[x8][y8])
            #print "============================================================="
    return dcta


def preproc():
    print "stream"

def rc5():
    print "stream"

def send():
    print "stream"

def enc():
    print "stream"

def dec():
    print "stream"

cap = cv2.VideoCapture(0)
cuk = defaultdict(dict)
cap.set(3, 320)
cap.set(4, 400)
#cap.set(3, 1600)
#cap.set(4, 900)
cap.set(11, 45)

while(True):
    ret, frame = cap.read()
    blockelate(frame)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
