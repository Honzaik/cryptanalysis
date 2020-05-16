import sys

sys.setrecursionlimit(10000)

outputS = '10111111010001110110110101100001010111011000111000010010010000101111111100011101101000001000011101001110000111110101110100010010111010000111110011011010100101011100100000111000101011111010111111100101111100111100000000011100010000101010011010101010111001101100011111001001001000010010110110010011100110000100101110111011100110110011010010001101011110100010011001111011010010001100111011111100011000100001111111011011001110011010010010101010111100010011001001001001000101010111000101100010111100101010100011001101110111101000000111111110100101110001101011000010011110101011111100111000100011010111000001110110110010011100100101001011011111101100000110010101111110001110110010010001111010111111000101110101110010010111111001110001111001111000000110111110111001111100111100000001010110011001101111011011010000111011011101111010101100011010011101111010001010010000101000000011111111010100110011100010100101000001100010110001101101100000101110010011111101110101001101000100111100010100001000000000000011101110001010001101101110010011110100101111001010100100010010111111000111111101111010000100111111001011001001000111000010100110111111110100011100110001101101011000110111011011011001101001100111000011111100000100010101010010001111100110100110000001100001111111101011100010010101111100101110111011110001101110100110100001110001110111000011011001101000101111100010100000100010100100011111011101001001000111110010011111000111100010000110111010000111110001011010000101011100100101111011110001010000110000110000101111111010101001000111011101111011010010010100101011011000001111001100001101010111100110011011000000111100101010011000000000110111111011010100111001100011101001100011011010100100111100100100110100000011110101010011011101011000110100010100101100010100001001111100000011011101010111010110110000001110111010010110010010010010000101011100100011101010100001000110001110010101100010010100100101010101001000111111001010011000100111101100011011001001000101010101110110011101100111000001001010111001000011' #this is the keystream 

xLength = 11
yLength = 7
zLength = 5

X = [0]*xLength #initialization of the LFSRs
Y = [0]*yLength
Z = [0]*zLength

Xcache = {} #helper "array" for faster computing this simple LFSR implementation (with recursion)
Ycache = {}
Zcache = {}

def getX(i): #calculates x_i
    if (i < 1):
        return None
    if (i <= xLength):
        return X[i-1]
    if (i not in Xcache):
        Xcache[i] = getX(i-2) ^ getX(i-11)
    return Xcache[i]

def getY(i): #calculates y_i
    if (i < 1):
        return None
    if (i <= yLength):
        return Y[i-1]
    if (i not in Ycache):
        Ycache[i] = getY(i-1) ^ getY(i-7)
    return Ycache[i]

def getZ(i): #calculates z_i
    if (i < 1):
        return None
    if (i <= zLength):
        return Z[i-1]
    if (i not in Zcache):
        Zcache[i] = getZ(i-2) ^ getZ(i-5)
    return Zcache[i]

def getS(i): #calculates s_i
    if (i < 1):
        return None
    else:
        return (getX(i)&getY(i)) ^ (getX(i)&getZ(i)) ^ (getY(i)&getZ(i))

def getFirstS(n): #returns string s_1 ... s_n
    s = ''
    for i in range(n):
        s += str(getS(i+1))
    return s

#these 3 following functions initialize LFSRs to initial values given by an decimal integer
def setX(ivX): #0-2^11-1 = 0x0-0x7ff, 
    for i in range(xLength):
        X[i] = (ivX >> i) & 1

def setY(ivY): #0-2^7-1 = 0x0-0x7f
    for i in range(yLength):
        Y[i] = (ivY >> i) & 1

def setZ(ivZ): #0-2^5-1 = 0x0-0x1f
    for i in range(zLength):
        Z[i] = (ivZ >> i) & 1


def getNumberOfMatchingIndices(str1, str2): #calculates length(str)-hamming distance of str1,str2,
    if len(str1) != len(str2):
        return None
    result = 0
    for i in range(len(str1)):
        if (str1[i] == str2[i]):
            result += 1
    return result


#correlation of every lfsr is 6/8

lengthToCheck = 120 #number of bits from the given output we will check the correlation on
#with 119 bits it also gives us one candidate for each LFSR, with less there are more candidates (for X)
strToCompare = outputS[:lengthToCheck] #slice the string for comparison

#bruteforce values for Z (32 values) and print candidates that match on > 65% of bits
for ivZ in range(0x20):
    Zcache = {}
    setZ(ivZ)
    zStream = ''
    for i in range(lengthToCheck):
        zStream += str(getZ(i+1))

    corr = float(getNumberOfMatchingIndices(zStream, strToCompare)) / lengthToCheck
    if(corr > 0.65): #expected correlation is 6/8 = 0.75
        print('z candidate:', ivZ)

#bruteforce values for Y (128 values) and print candidates that match on > 65% of bits
for ivY in range(0x80):
    Ycache = {}
    setY(ivY)
    yStream = ''
    for i in range(lengthToCheck):
        yStream += str(getY(i+1))

    corr = float(getNumberOfMatchingIndices(yStream, strToCompare)) / lengthToCheck
    if(corr > 0.65): #expected correlation is 6/8 = 0.75
        print('y candidate:', ivY)

#bruteforce values for X (2048 values) and print candidates that match on > 65% of bits
for ivX in range(0x800):
    Xcache = {}
    setX(ivX)
    xStream = ''
    for i in range(lengthToCheck):
        xStream += str(getX(i+1))

    corr = float(getNumberOfMatchingIndices(xStream, strToCompare)) / lengthToCheck
    if(corr > 0.65): #expected correlation is 6/8 = 0.75
        print('x candidate:', ivX)


#results
realXInt = 749
realYInt = 59
realZInt = 21


#check for correctness
setX(749)
setY(59)
setZ(21)

Xcache = {}
Ycache = {}
Zcache = {}
print(getFirstS(1000))
print(outputS[:1000])

'''
#bruteforce
for ivZ in range(0x20):
    setZ(ivZ)
    Zcache = {}
    print(str(ivZ))
    for ivY in range(0x80):
        setY(ivY)
        Ycache = {}
        for ivX in range(0x800):
            setX(ivX)
            Xcache = {}
            result = getFirstS(checkLength)
            if result == strToCompare:
                print('candidate: ivX: ' + str(ivX) + ', ivY: ' + str(ivY) + ', ivZ:' + str(ivZ))

#candidate: ivX: 749, ivY: 59, ivZ:21
'''