from PIL import Image
from collections import defaultdict
import math
import cv2
import socket
import numpy as np

def blockelate(xsize, ysize, frame):
    print frame[0][0]
    pix88r, pix88g, pix88b = {}, {}, {}
    pix88y, pix88cb,    pix88cr = {}, {}, {}
    dct88y, dct88cb, dct88cr = {}, {}, {}
    for pixy in range(int(xsize/8)):
        pix88r[pixy], pix88g[pixy], pix88b[pixy] = {}, {}, {}
        pix88y[pixy], pix88cb[pixy], pix88cr[pixy] = {}, {}, {}
        dct88y[pixy], dct88cb[pixy], dct88cr[pixy] = {}, {}, {}
        for pixx in range(int(ysize/8)):
            pix88r[pixy][pixx], pix88g[pixy][pixx], pix88b[pixy][pixx] = {}, {}, {}
            pix88y[pixy][pixx], pix88cb[pixy][pixx], pix88cr[pixy][pixx] = {}, {}, {}
            dct88y[pixy][pixx], dct88cb[pixy][pixx], dct88cr[pixy][pixx] = {}, {}, {}
            # print "\n\n\n========================BLOCK CHANGE========================"
            for py8 in range(8):
                pix88r[pixy][pixx][py8], pix88g[pixy][pixx][py8], pix88b[pixy][pixx][py8] = {}, {}, {}
                pix88y[pixy][pixx][py8], pix88cb[pixy][pixx][py8], pix88cr[pixy][pixx][py8] = {}, {}, {}
                dct88y[pixy][pixx][py8], dct88cb[pixy][pixx][py8], dct88cr[pixy][pixx][py8] = {}, {}, {}
                for px8 in range(8):
                    pix88r[pixy][pixx][py8][px8], pix88g[pixy][pixx][py8][px8], pix88b[pixy][pixx][py8][px8] = \
                        frame[(pixx * 8) + px8][(pixy * 8) + py8][0], frame[(pixx * 8) + px8][(pixy * 8) + py8][1], frame[(pixx * 8) + px8][(pixy * 8) + py8][2]
                    print "blok(y,x): " + str(pixy) + "," + str(pixx) + "  selblock(y,x): " + str(py8) + "," + str(px8) + \
                          "  R: " + str(pix88r[pixy][pixx][py8][px8]) + "  G: " + str(pix88g[pixy][pixx][py8][px8]) +"  B: " + str(pix88b[pixy][pixx][py8][px8])
                    pix88y[pixy][pixx][py8][px8], pix88cb[pixy][pixx][py8][px8], pix88cr[pixy][pixx][py8][px8] = \
                        toYCbCr(pix88r[pixy][pixx][py8][px8], pix88g[pixy][pixx][py8][px8], pix88b[pixy][pixx][py8][px8])
                    print "blok(y,x): " + str(pixy) + "," + str(pixx) + "  selblock(y,x): " + str(py8) + "," + str(px8) + \
                          "  Y: " + str(pix88y[pixy][pixx][py8][px8]) + "  Cb: " + str(
                        pix88cb[pixy][pixx][py8][px8]) + "  Cr: " + str(pix88cr[pixy][pixx][py8][px8])
            dct88y[pixy][pixx] = dct(pix88y[pixy][pixx])
            for py8 in range(8):
                for px8 in range(8):
                    print "DCT blok(y,x): " + str(pixy) + "," + str(pixx) + "  selblock(y,x): " + str(py8) + "," + str(px8) + " DCT: " + str(dct88y[pixy][pixx][py8][px8])

            if pixx % 4 == 0 and pixx != 0:
                ymail = blockenc(dct88y[pixy][pixx - 4], dct88y[pixy][pixx - 3], dct88y[pixy][pixx - 2], dct88y[pixy][pixx - 1])
                # cbmail = blockenc(dct88cb[pixy][pixx - 4], dct88cb[pixy][pixx - 3], dct88cb[pixy][pixx - 2], dct88cb[pixy][pixx - 1])
                # crmail = blockenc(dct88cr[pixy][pixx - 4], /dct88cr[pixy][pixx - 3], dct88cr[pixy][pixx - 2], dct88cr[pixy][pixx - 1])
                print ymail
                # print cbmail
                # print crmail
                # print "========================444444444========================"

def blockenc(block0, block1, block2, block3):
    dc = str(block0[0][0]) + 'z' + str(block1[0][0]) + 'z' + str(block2[0][0]) + 'z' + str(block3[0][0]) + 'z'
    ac4, encac4 = defaultdict(dict), defaultdict(dict)
    ac4[0] = str(quan(block0))
    ac4[1] = str(quan(block1))
    ac4[2] = str(quan(block2))
    ac4[3] = str(quan(block3))
    ac4 = ac4[0] + ac4[1] + ac4[2] + ac4[3]
    mail = str(dc) + str(ac4)
    return mail

def quan(block):
    ac = defaultdict(dict)
    ac[0] = (str(block[1][0]) + 'x' + str(block[0][1]) + 'x' + str(block[0][2]) + 'x' + str(block[1][1])) + 'y'
    ac[1] = (str(block[2][0]) + 'x' + str(block[3][0]) + 'x' + str(block[2][1]) + 'x' + str(block[1][2])) + 'y'
    ac[2] = (str(block[0][3]) + 'x' + str(block[0][4]) + 'x' + str(block[1][3]) + 'x' + str(block[2][2])) + 'yy'
    ac = ac[0] + ac[1] + ac[2]
    return ac

def toYCbCr(r, g, b):
    y = (0.299 * r) + (0.587 * g) + (0.114 * b)
    cb = -(0.1687 * r) - (0.3313 * g) + (0.5 * b) + 128
    cr = (0.5 * r) - (0.4187 * g) - (0.0813 * b) + 128
    # print y, cb, cr
    return y, cb, cr

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
                    sumc = sumc + sumct
            i, j = 1, 1
            if dx8 == 0:
                i = (2 ** -0.5)
            if dy8 == 0:
                j = (2 ** -0.5)
            dcty[dx8][dy8] = 0.25 * i * j * sumc
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
    return dcty

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
                    sumc = sumc + sumct
            dcta[x8][y8] = 0.25 * sumc
            dcta[x8][y8] = int(dcta[x8][y8])
            print str(x8), str(y8), str(dcta[x8][y8])
            #print "============================================================="
    return dcta

cap = cv2.VideoCapture(0)
cuk = defaultdict(dict)

while(True):
    ret, frame = cap.read()
    blockelate(640, 480, frame)
    print 'a'
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
