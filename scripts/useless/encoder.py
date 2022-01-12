import random as r

def e(str,sep,pad=' ',split=None): # encode 
  words=str.split(split)
  words=[w.rjust(len(max(words,key=len)),pad)for w in words]
  #print(words)
  prezip=[]
  for word in words:
    for i,c in enumerate(word):
      try:
        prezip[i]+=c
      except IndexError:
        prezip.append(c)
  prezip=sep.join(prezip)+f'\x03ETX{sep}{pad}{split or" "}'
  return prezip

def d(str,sep,pad=' ',split=' '): # decode with params
  return split.join([i.strip(pad)for i in[''.join(i)for i in zip(*str.split('\x03ETX')[0].split(sep))]])

def a(str): # decode with ETX magic
	m=str.split('\x03ETX');q=m[1]
	return q[2].join([i.strip(q[1])for i in[''.join(i)for i in zip(*m[0].split(q[0]))]])

def m(s,m): # mangler
	return s[0]+''.join([(r.randint(0,1)*m)+c for i,c in enumerate(s)if i!=0and i!=len(s)-1])+s[-1]

def generate_bytes_for_seed(seed: int, message: str) -> bytearray:
	r.seed(seed)
	result = bytearray()
	i = 0
	j = 0
	k = seed % 256  # iv for j
	# print(k)
	while i < len(message):
		c = message[i]
		if r.randrange(2):
			k = r.randrange(256)
			result.append(k ^ ord(c))
			i += 1
		else:
			j += k + i
			result.append(j % 256)
			# print(j)
	return result

def newline():
  print('')

## DOUBLE ESCAPE CONTROLS (\n \t etc.) OR USE RAW STRING

s='hi cark                           '

params={
	'sep':'-',
	'pad':'x',
	'split':'F',
}
seed = int(r.randint(0,1e5) )

enc=e(generate_bytes_for_seed(seed, s).hex().upper(),**params)+f'{{{seed}}}'
print(enc)
newline()

with open('encoder/outfile.txt','w')as file:file.write(enc)

# with open('outfile.txt','r') as file:
# 	exec(a(file.read()))

def make_autorun(infile,outfile='autorun.py'):
	with open(infile,'r') as inf, open(outfile,'w') as outf:
		# print(inf.read())
		outf.write(f"""import random as B
C={repr(inf.read())}.split('\\x03ETX')
A=C[1]
B.seed(int(A[4:-1]))
print(''.join((chr(B.randrange(256)^D)for D in bytes.fromhex((A[2]if len(A)>2 else' ').join([B.strip(A[1])for B in[''.join(B)for B in zip(*C[0].split(A[0]))]]))if B.randrange(2))))
""")

make_autorun('encoder/outfile.txt','encoder/autorun_file.py')


def make_autorun_no_infile(outfile='autorun.py'):
	with open(outfile,'w') as outf:
		outf.write(f"""import random as B
C={repr(enc)}.split('\\x03ETX')
A=C[1]
B.seed(int(A[4:-1]))
print(''.join((chr(B.randrange(256)^D)for D in bytes.fromhex((A[2]if len(A)>2 else' ').join([B.strip(A[1])for B in[''.join(B)for B in zip(*C[0].split(A[0]))]]))if B.randrange(2))))
""")

make_autorun_no_infile('encoder/autorun_otf.py')


# with open(infile,'r') as inf, open(outfile,'w') as outf:
# 	f"""import random
# 	D={repr(inf.read())}.split(\'\\x03ETX\');B=D[1]
# 	random.seed({seed})
# 	print(''.join(chr(random.randrange(256) ^ c)
# 			for c in bytes.fromhex({repr(generate_bytes_for_seed(seed, message).hex().upper())})
# 			if random.randrange(2)))
# 	"""