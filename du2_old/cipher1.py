sbox = [0x6,0x4,0xc,0x5,0x0,0x7,0x2,0xe,0x1,0xf,0x3,0xd,0x8,0xa,0x9,0xb]
inverseSbox = [0x4,0x8,0x6,0xa,0x1,0x3,0x0,0x5,0xc,0xe,0xd,0xf,0x2,0xb,0x7,0x9]

def encrypt(vstup, key):
	vystup = vstup ^ key[0]
	vystup = sbox[vystup]
	vystup = vystup ^ key[1]
	return vystup

secretKey = [0x5, 0x6]

pairs = []
for i in range(16):
	pairs.append([i,encrypt(i,secretKey)])



uDiff = pairs[2][0] ^ pairs[3][0]

#print(uDiff) #chci
candidateKeys = []

for keyGuess in range(16):
	diff = inverseSbox[keyGuess ^ pairs[2][1]] ^ inverseSbox[keyGuess ^ pairs[3][1]]
	if diff == uDiff:
		candidateKeys.append(keyGuess)

#new pair
uDiff = pairs[2][0] ^ pairs[8][0]

for keyGuess in candidateKeys:
	diff = inverseSbox[keyGuess ^ pairs[2][1]] ^ inverseSbox[keyGuess ^ pairs[8][1]]
	if diff == uDiff:
		print('first key: ' + str(keyGuess))
		key2 = keyGuess

secondKey = inverseSbox[pairs[0][1] ^ key2] ^ pairs[0][0]
print('second key: ' + str(secondKey))
