import random as r


def generate_bytes_for_seed(seed: int, message: str) -> bytearray:
    r.seed(seed)
    result = bytearray()
    i = 0
    j = 0
    k = seed % 256  # iv for j
    print(k)
    while i < len(message):
        c = message[i]
        if r.randrange(2):
            k = r.randrange(256)
            result.append(k ^ ord(c))
            i += 1
        else:
            j += k + i
            result.append(j % 256)
            print(j)
    return result


seed = int(r.random() * 10000)
message = "foo bar 12345 cark"
print(
    f"""import random
random.seed({seed})
print(''.join(chr(random.randrange(256) ^ c)
    for c in bytes.fromhex({repr(generate_bytes_for_seed(seed, message).hex().upper())})
    if random.randrange(2)))
"""
)
#
