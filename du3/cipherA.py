sbox = [0xf,0xe,0xb,0xc,0x6,0xd,0x7,0x8,0x0,0x3,0x9,0xa,0x4,0x2,0x1,0x5]

def encrypt(m, keys): #encryption function, encrypts m using keys 
    return sbox[m^keys[0]]^keys[1]

def getBitParity(m): #calculates number of 1s in a "binary" vector
    result = 0x0
    for i in range(4):
        result ^= (m >> i) & 0x1
    return result

alphaMask = 0b1001 #chosen mask alpha
betaMask = 0b0010 #choen mask beta

secretKeys = [0x1, 0x2] #0b0001, 0b0010 -> 1 + 1 = 0
print('we want to guess:', (getBitParity(alphaMask & secretKeys[0]) ^ getBitParity(betaMask & secretKeys[1]))) #the result of alpha x m + beta x c

numberOfKnownMessagePairs = 6 #number of messages used for attack

messagePairs = []
for i in range(numberOfKnownMessagePairs): #calculates some message pairs
    messagePairs.append([i, encrypt(i, secretKeys)])

t0 = 0
t1 = 0
for messagePair in messagePairs: # does the actual attack (calculates the counters)
    leftHandSideResult = 0x1 ^ getBitParity(alphaMask & messagePair[0]) ^ getBitParity(betaMask & messagePair[1])
    if (leftHandSideResult == 0):
        t0 += 1
    else:
        t1 += 1

print('counter t0:', t0)
print('counter t1:', t1)
print('the most probable result is:', int(t0 < t1))