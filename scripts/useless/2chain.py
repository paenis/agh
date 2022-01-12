import itertools
import string
import re


def shitty_de_bruijn(alpha, length=0, repeat=None):
    length = length or len(alpha)
    res = ""
    perms = sorted(
        [
            "".join(i)
            for i in {*itertools.permutations(alpha * (repeat or length), length)}
        ]
    )  # allow repeat
    for perm in perms:
        if perm in res:
            continue
        for c in perm:  # char by char
            res += c
            if perm in res:
                break
        print(res[-2 * length :])
    return re.sub(fr"(.)\1{{{length},}}", r"\1" * length, res)


def test(seq, alpha, length, repeat):
    failed = False
    for perm in {*itertools.permutations(alpha * (repeat or length), length)}:
        if "".join(perm) not in seq:
            print(f"failed! {''.join(perm)}\n\nsequence:\n{seq}")
            failed = True
            break
    if not failed:
        print(f"sequence is good! [a: '{alpha}', l: {length}, r: {repeat}]")


# string.ascii_lowercase
params = (" .,:;", 3, 3)
generated = shitty_de_bruijn(*params)

test(generated, *params)
print(generated)
print(f"len {len(generated)}\nopt {len(params[0])**params[1]}")
