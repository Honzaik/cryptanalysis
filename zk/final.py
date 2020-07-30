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

cipherInput = 0xabc1f1 #kazda cast musi bejt mod p

encrypted = encryptFeistel(cipherInput, roundKeys)

print(hex(encrypted))


decrypted = decryptFeistel(encrypted, roundKeys[::-1])

print(hex(decrypted))
print('------')

# attack

a = 0xb54
b = 0xc11

rightVal = (2 * a * b) % p

print(hex(rightVal))

#P1 = 0x19c254 # 
#P1 = randrange(0,0x1000000)


def doAttack(previousCandidates):
    P1 = randrange(0,0x1000000)
    P1L = (P1 & 0xfff000) >> 12 
    P2 = (P1 & 0x000fff) ^ (((P1L + a) % p) << 12)
    P3 = (P1 & 0x000fff) ^ (((P1L + b) % p) << 12)
    P4 = (P1 & 0x000fff) ^ (((P1L + a + b) % p) << 12)

    C1 = encryptFeistel(P1, roundKeys)
    C2 = encryptFeistel(P2, roundKeys)
    C3 = encryptFeistel(P3, roundKeys)
    C4 = encryptFeistel(P4, roundKeys)

    newCandidates = {}
    hasPreviousCandidates = False
    if (previousCandidates is not None):
        hasPreviousCandidates = True

    if (hasPreviousCandidates):
        k5GuessRange = previousCandidates.keys()
    else: 
        k5GuessRange = range(0x0, 0x1000)

    for k5Guess in k5GuessRange:
        D1 = feistelRound(C1, k5Guess, False)
        D2 = feistelRound(C2, k5Guess, False)
        D3 = feistelRound(C3, k5Guess, False)
        D4 = feistelRound(C4, k5Guess, False)

        D1L = (D1 & 0xfff000) >> 12
        D2L = (D2 & 0xfff000) >> 12
        D3L = (D3 & 0xfff000) >> 12
        D4L = (D4 & 0xfff000) >> 12

        D1R = D1 & 0xfff
        D2R = D2 & 0xfff
        D3R = D3 & 0xfff
        D4R = D4 & 0xfff

        temp = (D1L+D4L-D2L-D3L) % p

        if (hasPreviousCandidates):
            k4GuessRange = previousCandidates[k5Guess]
        else:
            k4GuessRange = range(0x0, 0x1000)

        for k4Guess in k4GuessRange:
            t1 = ((D1R + k4Guess)**2) % p
            t2 = ((D2R + k4Guess)**2) % p
            t3 = ((D3R + k4Guess)**2) % p
            t4 = ((D4R + k4Guess)**2) % p

            leftVal = (temp-(t1+t4-t2-t3))%p
            if (rightVal == leftVal):
                if (k5Guess in newCandidates):
                    newCandidates[k5Guess].append(k4Guess)
                else:
                    newCandidates[k5Guess] = [k4Guess]
                
        print(k5Guess)
    return newCandidates


candidates1 = doAttack(None)

print(candidates1)

candidates2 = doAttack(candidates1)

print(candidates2)