key1 = 0x1
key2 = 0x2

sbox = [0x4, 0x1, 0x3, 0x0, 0xf, 0x9, 0xa, 0x5, 0xd, 0xc, 0xb, 0xe, 0x6, 0x7, 0x2, 0x8]
revSbox = [0x3, 0x1, 0xe, 0x2, 0x0, 0x7, 0xc, 0xd, 0xf, 0x5, 0x6, 0xa, 0x9, 0x8, 0xb, 0x4]

def encrypt(data, key):
    return sbox[data ^ key] ^ key

def decrypt(data, key):
    return revSbox[data ^ key] ^ key

table = []

m = 0x0

for i in range(16):
    table.append([decrypt(m, i), i, 0])
cs = []
for value in table:
    cs.append(encrypt(decrypt(encrypt(value[0], key1), key2), key1))

for i in range(16):
    table.append([decrypt(cs[i], i), i, 1])

candidates1 = []

for i in range(16):
    for j in range(16, 32):
        if table[j][0] == table[i][0]:
            candidates1.append([i,j-16])

table = []

#check for a new message
m = 0x2

for i in range(16):
    table.append([decrypt(m, i), i, 0])
cs = []
for value in table:
    cs.append(encrypt(decrypt(encrypt(value[0], key1), key2), key1))

for i in range(16):
    table.append([decrypt(cs[i], i), i, 1])

candidates2 = []

for i in range(16):
    for j in range(16, 32):
        if table[j][0] == table[i][0]:
            candidates2.append([i,j-16])

intersection = []
for candidate in candidates1:
    if candidate in candidates2:
        intersection.append(candidate)

print('we have candicates: ' + str(intersection)) #2 candidate key pairs

#we now have only 2 possible keys, lets check which one encrypts "properly"
m = 0x6
c = encrypt(decrypt(encrypt(m, key1), key2), key1)
print('correct encryption: ' + str(c))
print('first candidate encryption: ' + str(encrypt(decrypt(encrypt(m, intersection[0][0]), intersection[0][1]), intersection[0][0])))
print('second candidate encryption ' + str(encrypt(decrypt(encrypt(m, intersection[1][0]), intersection[1][1]), intersection[1][0])))
print(str(intersection[0]) + ' is the correct key pair')
