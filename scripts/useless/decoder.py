import sys
with open(sys.argv[1], 'r') as file:
	string = file.read()

import random as B
C=string.split('\x03ETX')
A=C[1]
B.seed(int(A[4:-1]))
print(''.join((chr(B.randrange(256)^D)for D in bytes.fromhex((A[2]if len(A)>2 else' ').join([B.strip(A[1])for B in[''.join(B)for B in zip(*C[0].split(A[0]))]]))if B.randrange(2))))
