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
'''
# attack

a = 0xb54

#P1 = 0x19c254 # 
#P1 = randrange(0,0x1000000)

x = 0x514

P1 = x << 12
P2 = ((x + a) % p) << 12


print(hex(P1), hex(P2))

P1after1Round = feistelRound(P1, roundKeys[0], True)
P2after1Round = feistelRound(P2, roundKeys[0], True)

P1after2Round = feistelRound(P1after1Round, roundKeys[1], True)
P2after2Round = feistelRound(P2after1Round, roundKeys[1], True)

print(hex(P1after1Round), hex(P2after1Round))
print(hex(P1after2Round), hex(P2after2Round))

diff = (0x6d3-0x2a4)%p
diff = (diff - (a**2 + 2*a*x)) % p
print(hex(diff))

print('yyyyyyyyyyyyyy')

#P1 = 0x19c254 # 
#P1 = randrange(0,0x1000000)

x = 0xabc

P1 = x << 12
P2 = ((x + a) % p) << 12


print(hex(P1), hex(P2))

P1after1Round = feistelRound(P1, roundKeys[0], True)
P2after1Round = feistelRound(P2, roundKeys[0], True)

P1after2Round = feistelRound(P1after1Round, roundKeys[1], True)
P2after2Round = feistelRound(P2after1Round, roundKeys[1], True)

print(hex(P1after1Round), hex(P2after1Round))
print(hex(P1after2Round), hex(P2after2Round))

diff = (0x771-0x66b)%p
diff = (diff - (a**2 + 2*a*x)) % p
print(hex(diff))
'''
a = 0xb54

def doAttack(previousCandidates):
    x = randrange(0,0x1000)
    y = randrange(0,0x1000)
    P1 = x << 12
    P2 = ((x + a) % p) << 12
    P3 = y << 12
    P4 = ((y + a) % p) << 12

    toSubstract = (2 * x * a - 2 * y * a) % p

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

        leftVal = (D2L-D4L-D1L+D3L- toSubstract) % p

        if (hasPreviousCandidates):
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
