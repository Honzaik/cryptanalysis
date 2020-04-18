sbox = [0xf,0xe,0xb,0xc,0x6,0xd,0x7,0x8,0x0,0x3,0x9,0xa,0x4,0x2,0x1,0x5]
inverseSbox = [0x8,0xe,0xd,0x9,0xc,0xf,0x4,0x6,0x7,0xa,0xb,0x2,0x3,0x5,0x1,0x0]

def encrypt(m, keys): #encryption function, encrypts m using keys 
    return sbox[sbox[sbox[m^keys[0]]^keys[1]]^keys[2]]^keys[3]

def getBitParity(m): #calculates number of 1s in a "binary" vector
    result = 0x0
    for i in range(4):
        result ^= (m >> i) & 0x1
    return result

alphaMask = 0b1101 #chosen mask alpha
betaMask = alphaMask #chosen mask beta
gammaMask = alphaMask #chosen mask gamma

secretKeys = [0xe, 0x2, 0xf, 0x0]
print('we want to guess bit:', (getBitParity(alphaMask & secretKeys[0]) ^ getBitParity(betaMask & secretKeys[1]) ^ getBitParity(gammaMask & secretKeys[2]))) #the result of (k0+k1+k2)*d
print('and the k3:', hex(secretKeys[3]))
print('-----------------')

numberOfKnownMessagePairs = 12 #number of messages used for attack

messagePairs = []
for i in range(numberOfKnownMessagePairs): #calculates some message pairs
    messagePairs.append([i, encrypt(i, secretKeys)])

counters = []
for k3Guess in range(16):
    t0 = 0
    t1 = 0
    for messagePair in messagePairs: # does the actual attack (calculates the counters)
        invertedC = inverseSbox[messagePair[1] ^ k3Guess]
        leftHandSideResult = getBitParity(alphaMask & messagePair[0]) ^ getBitParity(gammaMask & invertedC)
        if (leftHandSideResult == 0):
            t0 += 1
        else:
            t1 += 1
    counters.append([t0, t1])

candidates = []
maxDifference = 0
for k3Guess in range(16):
    diff = abs(counters[k3Guess][0]-counters[k3Guess][1]) #calculate the difference between T_0 and T_1 corresponding to guessed k3
    if (diff > maxDifference): #if this key guess has bigger difference than any key before - reset candidates and set new maximum
        maxDifference = diff
        candidates = []

    if (diff == maxDifference): #append candidate since it has the biggest difference between T_0 and T_1
        candidate = [k3Guess, (counters[k3Guess][0] < counters[k3Guess][1])] #first entry is k3 candidate and second entry is corresponding (k0+k1+k2)*d value
        candidates.append(candidate)

for candidate in candidates:
    print('k3 candidate:', hex(candidate[0]), 'and the bit of keys k0,k1,k2:', int(candidate[1]))
