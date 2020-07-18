
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
