from random import randrange


p = 51043 #16 bit prime -> input 16bits = 2 bytes = 4 hex digits
#block size is 2*16 = 32 bits = 4 bytes =8 hex digits

def feistelRound(roundInput, roundKey):
    inputLeft = (roundInput & 0xffff0000) >> 16
    inputRight = (roundInput & 0xffff)
    #print(hex(roundInput))
    #print(hex(roundKey))
    #print(hex(inputLeft), hex(inputRight))
    outputLeft = inputRight
    roundFunctionOutput = ((inputRight + roundKey)**2) % p
    outputRight = inputLeft ^ roundFunctionOutput
    #print(hex(outputLeft))
    #print(hex(outputRight))
    return (outputLeft << 16) ^ outputRight

def switchSides(inputToSwitch):
    outputLeft = (inputToSwitch & 0xffff0000) >> 16
    outputRight = (inputToSwitch & 0xffff)
    return (outputRight << 16) ^ outputLeft

def encryptFeistel(plaintext, roundKeys):
    output = plaintext
    for i in range(len(roundKeys)):
        output = feistelRound(output, roundKeys[i])
    return switchSides(output)

roundKeys = [0xa4c7, 0x2ea5, 0x9aa2, 0x1298, 0xcc21]

cipherInput = 0xabcdef12

encrypted = encryptFeistel(cipherInput, roundKeys)

print(hex(encrypted))

decrypted = encryptFeistel(encrypted, roundKeys[::-1])

print(hex(decrypted))


# attack

a = 0xab54
b = 0xdc11
alpha = a << 16
beta = b << 16

rightVal = (2 * a * b) % p

P1 = 0x9c24544 # 
#P1 = randrange(0,0x10000000)

P2 = P1 ^ alpha
P3 = P1 ^ beta
P4 = P1 ^ alpha ^ beta


P1after1Round = feistelRound(P1, roundKeys[0])
P2after1Round = feistelRound(P2, roundKeys[0])
P3after1Round = feistelRound(P3, roundKeys[0])
P4after1Round = feistelRound(P4, roundKeys[0])

fOutput1 =  (((P1after1Round & 0xffff) + 0x2ea5)**2) % p
fOutput2 =  (((P2after1Round & 0xffff) + 0x2ea5)**2) % p
fOutput3 =  (((P3after1Round & 0xffff) + 0x2ea5)**2) % p
fOutput4 =  (((P4after1Round & 0xffff) + 0x2ea5)**2) % p

P1Rafter2Round = ((P1after1Round & 0xffff0000) >> 16) ^ fOutput1
P2Rafter2Round = ((P2after1Round & 0xffff0000) >> 16) ^ fOutput2
P3Rafter2Round = ((P3after1Round & 0xffff0000) >> 16) ^ fOutput3
P4Rafter2Round = ((P4after1Round & 0xffff0000) >> 16) ^ fOutput4


C1 = encryptFeistel(P1, roundKeys)
C2 = encryptFeistel(P2, roundKeys)
C3 = encryptFeistel(P3, roundKeys)
C4 = encryptFeistel(P4, roundKeys)


#k5Guess = 0xcc21

for k5Guess in range(0,0x10000):
    D1 = feistelRound(C1, k5Guess)
    D2 = feistelRound(C2, k5Guess)
    D3 = feistelRound(C3, k5Guess)
    D4 = feistelRound(C4, k5Guess)

    D1L = (D1 & 0xffff0000) >> 16
    D2L = (D2 & 0xffff0000) >> 16
    D3L = (D3 & 0xffff0000) >> 16
    D4L = (D4 & 0xffff0000) >> 16

    D1R = D1 & 0xffff
    D2R = D2 & 0xffff
    D3R = D3 & 0xffff
    D4R = D4 & 0xffff

    temp = D1L^D4L^D2L^D3L
    for k4Guess in range(0, 0x10000):
        t1 = (((D1R + k4Guess) % p)**2) % p
        t2 = (((D2R + k4Guess) % p)**2) % p
        t3 = (((D3R + k4Guess) % p)**2) % p
        t4 = (((D4R + k4Guess) % p)**2) % p



        leftVal = t1^t4^t2^t3^temp
        if (rightVal == leftVal):
            print(hex(k4Guess), hex(k5Guess))
