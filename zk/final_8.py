from random import randrange


p = 4013 #12 bit prime -> input 12bits = 3 hex digits
#block size is 2*12 = 24 bits  = 6 hex digits

def feistelRound(roundInput, roundKey, encrypt):
    inputLeft = (roundInput & 0xfff000) >> 12
    inputRight = (roundInput & 0xfff)
    outputLeft = inputRight
    roundFunctionOutput = ((inputRight + roundKey)**2) % p

    if (encrypt):
        outputRight = (inputLeft + roundFunctionOutput) % p
    else:
        outputRight = (inputLeft - roundFunctionOutput) % p

    return (outputLeft << 12) ^ outputRight

def switchSides(inputToSwitch):
    outputLeft = (inputToSwitch & 0xfff000) >> 12
    outputRight = (inputToSwitch & 0xfff)
    return (outputRight << 12) ^ outputLeft

def encryptFeistel(plaintext, roundKeys):
    output = plaintext
    for i in range(len(roundKeys)):
        output = feistelRound(output, roundKeys[i], True)
    return switchSides(output)

def decryptFeistel(ciphertext, roundKeys):
    output = ciphertext
    for i in range(len(roundKeys)):
        output = feistelRound(output, roundKeys[i], False)
    return switchSides(output)

roundKeys = [0xa4c, 0x2ea, 0x9a, 0x129, 0xcc2]

a = 0xb54

def doAttack(previousCandidates):
    x = randrange(0,0x1000) # generate random part of the first plaintext
    y = randrange(0,0x1000) # generate random part of the second plaintext
    P1 = x << 12 # x||0
    P2 = ((x + a) % p) << 12 # x+a || 0
    P3 = y << 12 # y || 0
    P4 = ((y + a) % p) << 12 # y+a || 0

    toSubstract = (2 * x * a - 2 * y * a) % p #we calculate the part which we will substract for every k5, k4 guess here so it is not calculated every loop

    C1 = encryptFeistel(P1, roundKeys) # we encrypt those 4 plaintexts
    C2 = encryptFeistel(P2, roundKeys)
    C3 = encryptFeistel(P3, roundKeys)
    C4 = encryptFeistel(P4, roundKeys)

    newCandidates = {}
    hasPreviousCandidates = False
    if (previousCandidates is not None):
        hasPreviousCandidates = True

    if (hasPreviousCandidates): # if we are doing this attack for a new set of plaintexts and we already have some candidate set, we will only loop through that set to make it efficient
        k5GuessRange = previousCandidates.keys()
    else: 
        k5GuessRange = range(0x0, 0x1000)

    for k5Guess in k5GuessRange:
        D1 = feistelRound(C1, k5Guess, False) #undo the last round of encryption
        D2 = feistelRound(C2, k5Guess, False)
        D3 = feistelRound(C3, k5Guess, False)
        D4 = feistelRound(C4, k5Guess, False)

        D1L = (D1 & 0xfff000) >> 12 #get the left part 
        D2L = (D2 & 0xfff000) >> 12
        D3L = (D3 & 0xfff000) >> 12
        D4L = (D4 & 0xfff000) >> 12

        D1R = D1 & 0xfff #get the right part
        D2R = D2 & 0xfff
        D3R = D3 & 0xfff
        D4R = D4 & 0xfff

        leftVal = (D2L-D4L-D1L+D3L- toSubstract) % p # we precalculate this part of the difference which we will compare 

        if (hasPreviousCandidates): # same thing as with preexisting candidates keys k5 but for the keys k4
            k4GuessRange = previousCandidates[k5Guess]
        else:
            k4GuessRange = range(0x0, 0x1000)

        for k4Guess in k4GuessRange:
            t1 = ((D1R + k4Guess)**2) % p
            t2 = ((D2R + k4Guess)**2) % p
            t3 = ((D3R + k4Guess)**2) % p
            t4 = ((D4R + k4Guess)**2) % p

            rightVal = (t3-t4-t1+t2) % p 
            if (rightVal == leftVal):# (D2L-t2)-(D1L-t1)-(a^2+2ax) == (D4l-t4)-(D3L-t3)-(a^2+2ay) <=> f(x+a+f(k1)+k2)-f(x+f(k1)+k2) - (a^2+2ax) == f(y+a+f(k1)+k2)-f(y+f(k1)+k2) - (a^2+2ay)
                #add a new key pair into a dictionary, there can be multiple keys k4 for a k5 guess
                if (k5Guess in newCandidates):
                    newCandidates[k5Guess].append(k4Guess)
                else:
                    newCandidates[k5Guess] = [k4Guess]
    return newCandidates


candidates1 = doAttack(None)
candidates2 = doAttack(candidates1)
#candidates2 should have only one candidate key pair

for candidate in candidates2:
    print('k4:', hex(candidates2[candidate][0]), 'k5:', hex(candidate))

