import requests as r

get = r.get(
    'https://roambarcelona.com/clock-pt1?verify=Na2Q%2BeqhSP5hTRLDwpTNoA%3D%3D'
).content + r.get(
    'https://roambarcelona.com/clock-pt2?verify=Na2Q%2BeqhSP5hTRLDwpTNoA%3D%3D'
).content + r.get(
    'https://roambarcelona.com/clock-pt3?verify=Na2Q%2BeqhSP5hTRLDwpTNoA%3D%3D'
).content + r.get(
    'https://roambarcelona.com/clock-pt4?verify=Na2Q%2BeqhSP5hTRLDwpTNoA%3D%3D'
).content + r.get(
    'https://roambarcelona.com/clock-pt5?verify=Na2Q%2BeqhSP5hTRLDwpTNoA%3D%3D'
).content
print(get.decode())
post = r.post(
    f'https://roambarcelona.com/get-flag?verify=Na2Q%2BeqhSP5hTRLDwpTNoA%3D%3D&string={get.decode()}'
).content
print(post.decode())

#####

def nextPermutation(perm):
    k0 = None
    for i in range(len(perm) - 1):
        if perm[i] < perm[i + 1]:
            k0 = i
    if k0 == None:
        return None

    l0 = k0 + 1
    for i in range(k0 + 1, len(perm)):
        if perm[k0] < perm[i]:
            l0 = i

    perm[k0], perm[l0] = perm[l0], perm[k0]
    perm[k0 + 1:] = reversed(perm[k0 + 1:])
    return perm


*perm, = "2457"
while perm:
    print(''.join(perm))
    perm = nextPermutation(perm)

#####

n = 4096
for i in range(1, 5521):
    n += i

print(n)

#####

filenames = ['locks', 'locks_old']
with open('concat', 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            outfile.write(infile.read() + '\n')

#####

from Crypto.Cipher import AES
import base64

BLOCK_SIZE = 32

PADDING = '{'

# Encrypted text to decrypt
encrypted = "uqX82PBZ8pi1fvt4GLHYgLs50ht8OQlrR1KHL2teppQ="


def DecodeAES(c, e):
    try:
        return c.decrypt(base64.b64decode(e)).decode().rstrip(PADDING)
    except UnicodeDecodeError:
        return ''


secrets = [i.rstrip() for i in open('words.txt', 'r').readlines()]

for secret in secrets:
    if (secret[-1:] == "\n"):
        print(
            "Error, new line character at the end of the string. This will not match!"
        )
    elif (len(secret.encode('utf-8')) >= 32):
        print("Error, string too long. Must be less than 32 bytes.")
    else:
        # create a cipher object using the secret
        cipher = AES.new(
            secret +
            (BLOCK_SIZE - len(secret.encode('utf-8')) % BLOCK_SIZE) * PADDING)

        # decode the encoded string
        decoded = DecodeAES(cipher, encrypted)

        if (decoded.startswith('FLAG:')):
            print("\n")
            print("Success: " + secret + "\n")
            print(decoded + "\n")
            break
        else:
            pass
