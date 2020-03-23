key1 = 0x1
key2 = 0x3

sbox = [0x4, 0x1, 0x3, 0x0, 0xf, 0x9, 0xa, 0x5, 0xd, 0xc, 0xb, 0xe, 0x6, 0x7, 0x2, 0x8]
revSbox = [0x3, 0x1, 0xe, 0x2, 0x0, 0x7, 0xc, 0xd, 0xf, 0x5, 0x6, 0xa, 0x9, 0x8, 0xb, 0x4]

def encrypt(data, key):
    return sbox[data ^ key]

def decrypt(data, key):
    return revSbox[data] ^ key

table1 = []

#first pair
m1 = 0x4
c1 = encrypt(encrypt(m1, key1), key2)

for i in range(16):
    table1.append(encrypt(m1, i))

candidates = []

for i in range(16):
    decrypted = decrypt(c1, i)
    keypair = [table1.index(decrypted), i]
    candidates.append(keypair)

#we now have our candidate keys from first pair, lets check another one to narrow the set

table2 = []

m2 = 0x5
c2 = encrypt(encrypt(m2, key1), key2)

for i in range(16):
    table2.append(encrypt(m2, i))

candidates2 = []

for i in range(16):
    decrypted = decrypt(c2, i)
    keypair = [table2.index(decrypted), i]
    candidates2.append(keypair)

intersection = []
for candidate in candidates:
    if candidate in candidates2:
        intersection.append(candidate)

print('we have candicates: ' + str(intersection)) #2 candidate key pairs

#we now have only 2 possible keys, lets check which one encrypts "properly"
m3 = 0x6
c3 = encrypt(encrypt(m3, key1), key2)
print('correct encryption: ' + str(c3))
print('first candidate encryption: ' + str(encrypt(encrypt(m3, intersection[0][0]), intersection[0][1])))
print('second candidate encryption ' + str(encrypt(encrypt(m3, intersection[1][0]), intersection[1][1])))

print(str(intersection[0]) + ' is the correct key pair')

