sbox = [0xf,0xe,0xb,0xc,0x6,0xd,0x7,0x8,0x0,0x3,0x9,0xa,0x4,0x2,0x1,0x5]
inverseSbox = [0x8,0xe,0xd,0x9,0xc,0xf,0x4,0x6,0x7,0xa,0xb,0x2,0x3,0x5,0x1,0x0]
permutace = [0x0,0x4,0x8,0xc,0x1,0x5,0x9,0xd,0x2,0x6,0xa,0xe,0x3,0x7,0xb,0xf]

#permutation used in the cipher
def permute(vstup):
    temp = 0x0
    for i in range(16):
        temp = temp ^ (((vstup >> i) & 0x1) << (permutace[i]))

    vstup = temp
    return vstup

#a round of the encryption function
def eRound(vstup, roundKey):
    vystup = vstup ^ roundKey
    vystup = sbox[vystup & 0x000f] ^ (sbox[(vystup & 0x00f0) >> 4] << 4) ^ (sbox[(vystup & 0x0f00) >> 8] << 8) ^ (sbox[(vystup & 0xf000) >> 12] << 12)
    vystup = permute(vystup)
    return vystup

#our encryption function
def encrypt(vstup, roundKeys):
    vystup = vstup
    for i in range(len(roundKeys) - 2):
        vystup = eRound(vystup, roundKeys[i])

    vystup = vystup ^ roundKeys[len(roundKeys)-2]
    vystup = sbox[vystup & 0x000f] ^ (sbox[(vystup & 0x00f0) >> 4] << 4) ^ (sbox[(vystup & 0x0f00) >> 8] << 8) ^ (sbox[(vystup & 0xf000) >> 12] << 12)
    vystup = vystup ^ roundKeys[len(roundKeys)-1]
    return vystup

#function which implements inverse sbox for input
def invertSbox(vstup):
    return inverseSbox[vstup & 0x000f] ^ (inverseSbox[(vstup & 0x00f0) >> 4] << 4) ^ (inverseSbox[(vstup & 0x0f00) >> 8] << 8) ^ (inverseSbox[(vstup & 0xf000) >> 12] << 12)

def getBitParity(m): #calculates number of 1s in a "binary" vector
    result = 0x0
    for i in range(16):
        result ^= (m >> i) & 0x1
    return result

secretRoundKeys = [0x1b1b, 0xe2e2, 0x2354, 0xbf45, 0xba45]; #secret round keys chosen by random
print('we want to guess first part of the k4 which is:', hex(secretRoundKeys[4]>>12))

mask = 0x8000 #given to us in the book

numberOfKnownMessagePairs = 64 #sufficiently large to give us just one candidate in most tries

messagePairs = []
for i in range(numberOfKnownMessagePairs): #calculates some message pairs
    messagePairs.append([i, encrypt(i, secretRoundKeys)])

counters = []
for k4GuessPart in range(16):
    k4Guess = k4GuessPart << 12 #tranform it into 16bit key 0x?000
    t0 = 0
    t1 = 0
    for messagePair in messagePairs:
        invertedC = invertSbox(messagePair[1]^k4Guess) #invert last round
        parity = getBitParity(messagePair[0] & mask) ^ getBitParity(invertedC & mask) #calculate parity on the sbox
        if (parity == 0):
            t0 += 1
        else:
            t1 += 1
    counters.append([t0, t1])


candidates = []
maxDifference = 0
for k4GuessPart in range(16):
    diff = abs(counters[k4GuessPart][0]-counters[k4GuessPart][1]) #calculate the difference between T_0 and T_1 corresponding to guessed k4 part
    if (diff > maxDifference): #if this key guess has bigger difference than any key before - reset candidates and set new maximum
        maxDifference = diff
        candidates = []

    if (diff == maxDifference): #append candidate since it has the biggest difference between T_0 and T_1
        candidates.append(k4GuessPart)

for candidate in candidates:
    print('k4 candidate:', hex(candidate))
