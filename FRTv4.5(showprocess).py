#able to send
#not encrypted
from collections import defaultdict
import math
import cv2
import socket

def send(ym, cbm, crm):
    raw = str(1) + ym + str(2) + cbm + str(3) + crm
    print raw
    # con.sendall(raw)

def blockelate(frame):
    print frame[0][0]
    frame[0][0] = 255,255,255
    for p in range(200, 232):
        for l in range(100, 132):
            frame[l][p] = toYCbCr(frame[l][p])[0]
            frame[l+50][p] = toYCbCr(frame[l+50][p])[1]
            frame[l+100][p] = toYCbCr(frame[l+100][p])[2]


    piycc = {}
    dcty = {}
    for pixy in range(4):
        piycc[pixy] = {}
        dcty[pixy] = {}
        for pixx in range(4):
            piycc[pixy][pixx] = {}
            dcty[pixy][pixx] = {}
            for py8 in range(8):
                dcty[pixy][pixx][py8] = {}
                piycc[pixy][pixx][py8] = {}
                for px8 in range(8):
                    dcty[pixy][pixx][py8][px8] = {}
                    piycc[pixy][pixx][py8][px8] = toYCbCr(frame[(pixx * 8) + 100][(pixy * 8) + 100])
            dcty[pixy][pixx] = dct(piycc[pixy][pixx])

            for py8 in range(8):
                for px8 in range(8):
                    print dcty[pixy][pixx][py8][px8]
                    frame[(pixx * 8) + 100 + px8][(pixy * 8) + 100 + py8] = dcty[pixy][pixx][py8][px8][0], dcty[pixy][pixx][py8][px8][0], dcty[pixy][pixx][py8][px8][0]
                    frame[(pixx * 8) + 150 + px8][(pixy * 8) + 100 + py8] = dcty[pixy][pixx][py8][px8][1], \
                                                                            dcty[pixy][pixx][py8][px8][1], \
                                                                            dcty[pixy][pixx][py8][px8][1]
                    frame[(pixx * 8) + 200 + px8][(pixy * 8) + 100 + py8] = dcty[pixy][pixx][py8][px8][2], \
                                                                            dcty[pixy][pixx][py8][px8][2], \
                                                                            dcty[pixy][pixx][py8][px8][2]
                     # = dcty[pixy][pixx][py8][px8][0]
                    # frame[(pixx * 8) + 100 + px8][(pixy * 8) + 100 + py8] = dcty[pixy][pixx][py8][px8][1]
                    # frame[(pixx * 8) + 100 + px8][(pixy * 8) + 100 + py8] = dcty[pixy][pixx][py8][px8][2]

    # ymail, cbmail, crmail = blockenc(dcty[0][0], dcty[0][1], dcty[1][0], dcty[1][1])
    # send(ymail, cbmail, crmail)

def recv(mail):
    print mail


def blockenc(block0, block1, block2, block3):
    dcy = str(block0[0][0][0]) + 'z' + str(block1[0][0][0]) + 'z' + str(block2[0][0][0]) + 'z' + str(
        block3[0][0][0]) + 'z'
    dccb = str(block0[0][0][1]) + 'z' + str(block1[0][0][1]) + 'z' + str(block2[0][0][1]) + 'z' + str(
        block3[0][0][1]) + 'z'
    dccr = str(block0[0][0][0]) + 'z' + str(block1[0][0][1]) + 'z' + str(block2[0][0][1]) + 'z' + str(
        block3[0][0][1]) + 'z'

    conact, encac4 = {}, {}
    for r in range(3):
        ac40 = str(quan(block0, r))
        ac41 = str(quan(block1, r))
        ac42 = str(quan(block2, r))
        ac43 = str(quan(block3, r))
        conact[r] = ac40 + ac41 + ac42 + ac43
        print conact[r]

    maily = dcy + conact[0]
    mailcb = dccb + conact[1]
    mailcr = dccr + conact[2]
    return maily, mailcb, mailcr

def quan(block, r):
    ac = (str(block[1][0][r]) + 'x' + str(block[0][1][r]) + 'x' + str(block[0][2][r]) + 'x' + str(block[1][1][r])) + 'y'
    return ac


def toYCbCr((r, g, b)):
    y = (0.299 * r) + (0.587 * g) + (0.114 * b)
    cb = -(0.1687 * r) - (0.3313 * g) + (0.5 * b) + 128
    cr = (0.5 * r) - (0.4187 * g) - (0.0813 * b) + 128
    return (y, cb, cr)


def toRGB(y, cb, cr):
    r = y + (1.402 * (cr - 128))
    g = y - (0.34414 * (cb - 128)) - (0.71414 * (cr - 128))
    b = y + (1.772 * (cb - 128))
    print r, g, b
    return r, g, b


def dct(block):
    dcty = {}
    r = {}
    for dy8 in range(8):
        dcty[dy8] = {}
        for dx8 in range(8):
            dcty[dy8][dx8] = {}
            sumy, sumcb, sumcr = 0, 0, 0
            for y8 in range(8):
                for x8 in range(8):
                    sumyt = block[y8][x8][0] * math.cos(((2 * x8 + 1) * dx8 * math.pi) / 16) * math.cos(
                        ((2 * y8 + 1) * dy8 * math.pi) / 16)
                    sumy = sumy + sumyt
                    sumcbt = block[y8][x8][1] * math.cos(((2 * x8 + 1) * dx8 * math.pi) / 16) * math.cos(
                        ((2 * y8 + 1) * dy8 * math.pi) / 16)
                    sumcb = sumcb + sumcbt
                    sumcrt = block[y8][x8][2] * math.cos(((2 * x8 + 1) * dx8 * math.pi) / 16) * math.cos(
                        ((2 * y8 + 1) * dy8 * math.pi) / 16)
                    sumcr = sumcr + sumcrt
            i, j = 1, 1
            if dx8 == 0:
                i = (2 ** -0.5)
            if dy8 == 0:
                j = (2 ** -0.5)

            dcty[dy8][dx8] = (0.25 * i * j * sumy), (0.25 * i * j * sumcb), (0.25 * i * j * sumcr)

            for gil in range(3):
                r[gil] = dcty[dy8][dx8][gil]
                if dcty[dy8][dx8][gil] > 0:
                    if dcty[dy8][dx8][gil] % 1 > 0.5 and dcty[dy8][dx8][gil] % 1 < 1:
                        r[gil] = int(dcty[dy8][dx8][gil]) + 1
                    if dcty[dy8][dx8][gil] % 1 <= 0.5 and dcty[dy8][dx8][gil] % 1 > 0:
                        r[gil] = int(dcty[dy8][dx8][gil])
                elif dcty[dy8][dx8][gil] < 0:
                    if dcty[dy8][dx8][gil] % -1 >= -0.5 and dcty[dy8][dx8][gil] % -1 < 0:
                        r[gil] = int(dcty[dy8][dx8][gil])
                    if dcty[dy8][dx8][gil] % -1 < -0.5 and dcty[dy8][dx8][gil] % -1 > -1:
                        r[gil] = int(dcty[dy8][dx8][gil]) - 1

            dcty[dy8][dx8] = (int(r[0]), int(r[1]), int(r[2]))
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
    return dcta


def preproc():
    print "stream"

def rc5():
    print "stream"

def enc():
    print "stream"

def dec():
    print "stream"


cap = cv2.VideoCapture(0)
cuk = defaultdict(dict)
cap.set(3, 720)
cap.set(4, 400)
# cap.set(3, 1600)
# cap.set(4, 900)
cap.set(11, 45)

server = '127.0.0.1'
port = 9001

colokan = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
colokan.bind((server, port))

# colokan.listen(1)
# con, addr = colokan.accept()

while (True):
    ret, frame = cap.read()
    blockelate(frame)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
