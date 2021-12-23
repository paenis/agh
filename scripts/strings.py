#!/usr/bin/env python

import subprocess as sp

strings=sp.run(['strings','./strings3-x86'],stdout=sp.PIPE)

stringarr=strings.stdout.decode().split('\n')
for i,s in enumerate(stringarr):
	print(f'Trying: {s} ({i}/{len(stringarr)})')
	try:
		proc=sp.run(['./strings3-x86',s],stdout=sp.PIPE,timeout=0.05)
	except sp.TimeoutExpired:
		print(f'Done! [{s}]')
		break
