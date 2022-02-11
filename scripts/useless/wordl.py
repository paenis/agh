# very bad wordle solver thing
print('loading...',end='')
import zlib, base64
with open('wordlist.txt', 'r') as file:
    exec(zlib.decompress(base64.b85decode(file.read())))

with open('morewords.txt', 'r') as file:
    exec(file.read())

orig_target = target + target2
orig_target = [*{*orig_target}]  # dedup
orig_target = [word for word in orig_target if '*' not in word]


all_words = valid + orig_target

include = set()
exclude = set()
print('done')
print('CANNOT handle double letters')
while True:
    w = input('>')  # word,status
    if ',' not in w:
        if w == 'reset':
            include = set()
            exclude = set()
            print('\033c')
        elif w == 'include':
            print(include)
        elif w == 'exclude':
            print(exclude)
        else:
            print('invalid command')
        continue

    w = [*map(str.strip, w.split(','))]
    if not all([c in 'gyb' for c in w[1]]) or len(w[1]) != len(w[0]):
        print('bad status')
        continue
    # if w[0] not in all_words:
    # 	print('invalid word')
    # 	continue
    stat_zip = [*zip(w[0], w[1])]
    for t in stat_zip:
        if t[1] in 'yg' and t[0] not in include:
            print(f'including {t[0]}')
            include.add(t[0])
        elif t[1] == 'b' and t[0] not in include:
            print(f'excluding {t[0]}')
            exclude.add(t[0])

    # same length
    target = [word for word in orig_target if len(word) == len(w[0])]
    # include/exclude
    include_list = [
        word for word in target if all([char in word for char in include])
    ]
    # print(include_list)
    exclude_list = [
        word for word in target if any([char in word for char in exclude])
    ]
    # print(exclude_list)

    # TODO: positional
    positional_exclude = []
    inter = [word for word in include_list if word not in exclude_list]
    # print(inter)
    for word in inter:
        for idx, char in enumerate(word):
            if w[1][idx] == 'g':  # good letter
                if not w[0][idx] == char:  # letter DOESN'T match
                    print(f'excluding {word} (green mismatch)')
                    positional_exclude.append(word)
                    break
            # if w[1][idx] == 'y': # maybe letter
            # 	if w[0][idx] == char: # letter DOES match
            # 		print(f'excluding {word} (yellow mismatch)')
            # 		positional_exclude.append(word)
            # 		break

    # print(positional_exclude)

    # print([word in exclude_list for word in include_list])
    good_list = [word for word in inter if word not in positional_exclude]
    print(good_list)
