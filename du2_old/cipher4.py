sbox = [0x6,0x4,0xc,0x5,0x0,0x7,0x2,0xe,0x1,0xf,0x3,0xd,0x8,0xa,0x9,0xb]
permutace = [0x0,0x4,0x8,0xc,0x1,0x5,0x9,0xd,0x2,0x6,0xa,0xe,0x3,0x7,0xb,0xf]
diffTable = [0]*16
for i in range(16):
	diffTable[i] = [0]*16

for i in range(16):
	inputDiff = i
	for j in range(16):
		outputDiff = sbox[j] ^ sbox[j^i]
		diffTable[i][outputDiff] = diffTable[i][outputDiff] + 1

#print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in diffTable]))


def permute(vstup):
    temp = 0x0
    for i in range(16):
        temp = temp ^ (((vstup >> i) & 0x1) << (permutace[i]))

    vstup = temp
    return vstup

def eRound(vstup, roundKey):
    vystup = vstup ^ roundKey
    vystup = sbox[vystup & 0x000f] ^ (sbox[(vystup & 0x00f0) >> 4] << 4) ^ (sbox[(vystup & 0x0f00) >> 8] << 8) ^ (sbox[(vystup & 0xf000) >> 12] << 12)
    vystup = permute(vystup)
    return vystup

def encrypt(vstup, roundKeys):
    vystup = vstup
    for i in range(len(roundKeys) - 2):
        vystup = eRound(vystup, roundKeys[i])

    print(hex(vystup))
    vystup = vystup ^ roundKeys[len(roundKeys)-2]
    vystup = sbox[vystup & 0x000f] ^ (sbox[(vystup & 0x00f0) >> 4] << 4) ^ (sbox[(vystup & 0x0f00) >> 8] << 8) ^ (sbox[(vystup & 0xf000) >> 12] << 12)
    vystup = vystup ^ roundKeys[len(roundKeys)-1]
    return vystup

print(hex(encrypt(0xaaaa,[0x1,0x2,0x3])))  