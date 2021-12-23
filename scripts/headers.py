#!/usr/bin/env python
wb=b'\xff\xd8\xff\xe0'

for i in range(1,9):
	ofile=f'./artwork-0{i}.jpg'
	nfile=f'./artwork-0{i}-mod-py.jpg'
	print(ofile)
	with open(ofile,'rb') as obuf,open(nfile,'wb') as nbuf:
		oread=obuf.read()
		# print(wb+oread)
		nbuf.write(wb+oread)
		print('success')