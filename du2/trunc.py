import random

sbox = [0x6,0x4,0xc,0x5,0x0,0x7,0x2,0xe,0x1,0xf,0x3,0xd,0x8,0xa,0x9,0xb]
inverseSbox = [0x4,0x8,0x6,0xa,0x1,0x3,0x0,0x5,0xc,0xe,0xd,0xf,0x2,0xb,0x7,0x9]
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

secretRoundKeys = [0x1b1b, 0xe2e2, 0x2354, 0x1f45, 0x1a45, 0xe4f5]; #secret round keys

#this function implements the attack
#iterations = number of different message pairs we will use (16*iterations) pairs in total
#lastKeyIndex = which nibble of the last key we want to get
#firstKeyPart = the guess for the part of the first key if we know it already (to simplify the progress)
def getCandidateKeyPairs(iterations, lastKeyIndex, firstKeyPart):
    counters = [] #array of counters - number of different counters = number of different random messages tried = iterations
    shiftValue = (3-lastKeyIndex)*4 #calculate shift based on lastKeyIndex = the index of the nibble of the last key
    if (firstKeyPart is None): #if we know first key (usually after first iteration) we can just work with this values instead of 16 possible values
        firstKeyGuessStart = 0
        firstKeyGuessStop = 16
    else:
        firstKeyGuessStart = firstKeyPart
        firstKeyGuessStop = firstKeyPart+1

    for iteration in range(iterations):
        randomValues = []
        for i in range(3): #generate random values for chosen messages
            randomValues.append(random.randrange(16))

        msgPairsByKey = {}
        for firstKeyPartGuess in range(firstKeyGuessStart, firstKeyGuessStop): #calculate the pairs of messages which have the difference 0x0020 after the first round for every key 
            firstKeyGuess = firstKeyPartGuess << 4 #0x00?0
            msgPairsByKey[firstKeyPartGuess] = []
            for i in range(16):
                chosenMsg = (randomValues[0] << 12) ^ (randomValues[1] << 8) ^ (i << 4) ^ randomValues[2]
                afterFirstRound = eRound(chosenMsg, firstKeyGuess)
                for j in range(16):
                    pairCandidate = (randomValues[0] << 12) ^ (randomValues[1] << 8) ^ (j << 4) ^ randomValues[2]
                    if afterFirstRound ^ eRound(pairCandidate, firstKeyGuess) == 0x0020:
                        msgPairsByKey[firstKeyPartGuess].append([chosenMsg, pairCandidate])

        cipherPairsByKey = {}
        for firstKeyPartGuess in range(firstKeyGuessStart, firstKeyGuessStop): #get encrypted pairs of the chosen messages
            cipherPairsByKey[firstKeyPartGuess] = []
            for pair in msgPairsByKey[firstKeyPartGuess]:
                cipherPairsByKey[firstKeyPartGuess].append([encrypt(pair[0], secretRoundKeys), encrypt(pair[1], secretRoundKeys)])


        counter = {} #dictionary which has an array for every first key
        for firstKeyPartGuess in range(firstKeyGuessStart, firstKeyGuessStop):
            counter[firstKeyPartGuess] = []
            for lastKeyPartGuess in range(16): #every guess of the "lastKeyIndex"th nibble of the last key
                counter[firstKeyPartGuess].append(0)
                lastKeyGuess = lastKeyPartGuess << shiftValue
                for pair in cipherPairsByKey[firstKeyPartGuess]:
                    invertedMsg1 = invertSbox(pair[0]^lastKeyGuess)
                    invertedMsg2 = invertSbox(pair[1]^lastKeyGuess)
                    differenceOnTheFirstSbox = ((invertedMsg1^invertedMsg2) & (0xf << shiftValue)) >> shiftValue
                    bitDifference = (differenceOnTheFirstSbox >> 2) & 0x1
                    if bitDifference == 0: #if the difference in 2nd bit is 0 increment counter. we can use this same logic for every nibble of the k5 because of the specific differential
                        counter[firstKeyPartGuess][lastKeyPartGuess] += 1

        counters.append(counter)

    candidates = [];
    for firstKeyPartGuess in range(firstKeyGuessStart, firstKeyGuessStop): #calculate which pairs have the perfect "counters". the real key will always have the difference 0x1 for every message (we have always 16 messages) in every iteration
        for lastKeyPartGuess in range(16):
            sumOfCounters = 0
            for counter in counters:
                sumOfCounters += counter[firstKeyPartGuess][lastKeyPartGuess]
            if sumOfCounters == 16*iterations:
                candidates.append([firstKeyPartGuess, lastKeyPartGuess])

    return candidates

print(getCandidateKeyPairs(4, 0, None)) #get candidates for first key part and also last key part (first part of the last key - index 0), 4 means that we will use 16*4 message pairs
print(getCandidateKeyPairs(4, 1, 1)) #using the knowledge we gain from the result above (we know the part of the first key is 0x1) we get candidates for the 2nd part of the last key
print(getCandidateKeyPairs(4, 2, 1)) # same as previous line but for 3rd part of the last key
print(getCandidateKeyPairs(4, 3, 1)) # 4th part of the last key

#in most iterations (the function above is random) we get only one candidate for the keys
