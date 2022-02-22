import random as r, argparse, os

FILE_OVERHEAD = 352

parser = argparse.ArgumentParser(usage="%(prog)s [-hvepd] [-s SEED] file [output]")

parser.add_argument("-v", "--verbose", help="print extra encoding info", action="store_true")
parser.add_argument("-e", "--exec", help="execute code in generated file (print by default)", action="store_true")
parser.add_argument("-p", "--print", help="print code to stdout", action="store_true")
parser.add_argument("-d", "--dryrun", help="don't output files (best used with -v)", action="store_true")
parser.add_argument("-s", "--seed", type=int, help="custom encoding seed")
parser.add_argument("file", type=str, help="file to encode ('-' for stdin)")
parser.add_argument("output", type=str, help="output path (cwd by default)", default=os.curdir, nargs="?")

args = parser.parse_args()


def e(str, sep, pad=" ", split=None):  # encode
    words = str.split(split)
    words = [w.rjust(len(max(words, key=len)), pad) for w in words]
    # print(words)
    prezip = []
    for word in words:
        for i, c in enumerate(word):
            try:
                prezip[i] += c
            except IndexError:
                prezip.append(c)
    prezip = sep.join(prezip) + f'\x03ETX{sep}{pad}{split or" "}'
    return prezip


def d(str, sep, pad=" ", split=" "):  # decode with params
    return split.join(
        [
            i.strip(pad)
            for i in ["".join(i) for i in zip(*str.split("\x03ETX")[0].split(sep))]
        ]
    )


def a(str):  # decode with ETX magic
    m = str.split("\x03ETX")
    q = m[1]
    return q[2].join(
        [i.strip(q[1]) for i in ["".join(i) for i in zip(*m[0].split(q[0]))]]
    )


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


if args.file != "-":
    with open(args.file, "r") as file:
        # global s
        s = file.read()
else:
    s = input()

params = {
    "sep": "-",
    "pad": "x",
    "split": "F",
}

seed = args.seed or r.randint(1e3, 1e4)

enc = e(generate_bytes_for_seed(seed, s).hex().upper(), **params) + f"{{{seed}}}"

# compress a bit
for i in zip(
    ("xx","aa","bb","cc","dd","ee","ff","gg","hh","ii","jj",),
    ("a","b","c","d","e","f","g","h","i","j","k",),
):
    enc = enc.replace(*i)

if args.verbose:
    print(
        *(
            enc,
            generate_bytes_for_seed(seed, s).hex().upper() + f"{{{seed}}}",
            f"size: {len(enc)/len(s):.02f}x ({(len(enc)+FILE_OVERHEAD)/len(s):.02f}x)",
        ),
        sep="\n\n",
        end="\n\n",
    )

if not args.dryrun:
    if not os.path.exists(args.output):
        os.mkdir(args.output)

    with open(os.path.join(args.output, "outfile.txt"), "w+") as file:
        file.write(enc)


def make_autorun(infile, outfile="autorun.py"):
    with open(infile, "r") as inf, open(outfile, "w+") as outf:
        # print(inf.read())
        outf.write(
            f"""import random as B
C={repr(inf.read())}
for A in zip('j i h g f e d c b a'.split(),'ii hh gg ff ee dd cc bb aa xx'.split()):C=C.replace(*A)
C=C.split('\\x03ETX')
A=C[1]
B.seed(int(A[4:-1]))
{'exec'if args.exec else'print'}(''.join((chr(B.randrange(256)^D)for D in bytes.fromhex((A[2]if len(A)>2else' ').join([B.strip(A[1])for B in[''.join(B)for B in zip(*C[0].split(A[0]))]]))if B.randrange(2))))
"""
        )


def make_autorun_no_infile(outfile="autorun.py"):
    with open(outfile, "w+") as outf:
        outf.write(
            f"""import random as B
C={repr(enc)}
for A in zip('j i h g f e d c b a'.split(),'ii hh gg ff ee dd cc bb aa xx'.split()):C=C.replace(*A)
C=C.split('\\x03ETX')
A=C[1]
B.seed(int(A[4:-1]))
{'exec'if args.exec else'print'}(''.join((chr(B.randrange(256)^D)for D in bytes.fromhex((A[2]if len(A)>2else' ').join([B.strip(A[1])for B in[''.join(B)for B in zip(*C[0].split(A[0]))]]))if B.randrange(2))))
"""
        )


if not args.dryrun:
    make_autorun_no_infile(os.path.join(args.output, "autorun_otf.py"))

    if args.print:
        with open(os.path.join(args.output, "autorun_otf.py"), "r") as file:
            print(file.read())

    print(f"done! wrote to {os.path.join(args.output,'autorun_otf.py')}")
else:
    print("done!")
