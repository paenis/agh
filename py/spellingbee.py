#!/usr/bin/env python

import json, string, os
from typing import List, Dict, Any  # lol

if os.path.exists('dictionary.json'):
    with open('dictionary.json', 'r') as handle:
        wordlist = json.load(handle)
else:
    # if dictionary doesn't exist, get one
    import requests
    # wordlist by https://github.com/lynn; any other json in the same format can be used
    with requests.get(
      'https://raw.githubusercontent.com/lynn/hello-wordl/main/src/' \
      'dictionary.json'
      ) as r:
        wordlist = r.json()
        # save the file for next time
        with open('dictionary.json', 'w') as handle:
            handle.write(r.text)


# convenience
def println(*s: List[str], **kwargs: Dict[str, Any]) -> None:
    print(
        *s,
        **kwargs,
        end='\n\n',
    )


# main func
def find_words(letters: str) -> None:
    include = required = None
    if not letters:  # string empty
        println('Please specify a string!')
        return
    if not all(c in (string.ascii_lowercase + '/') for c in letters):
        println('Please use only letters! (a-z, A-Z)')
        return

    if '/' in letters:
        include, required = letters.split('/')
        include_list = []
        for word in wordlist:
            if all(char in (include + required) for char in
                   word):  # need to include required letters as well
                if all(char in word for char in required):
                    include_list.append(word)
    else:
        include = letters
        include_list = []
        for word in wordlist:
            if all(char in include for char in word):
                include_list.append(word)

    if len(include_list) == 0:
        println('No words found!')
    else:
        println(*include_list, sep=', ')


def mainloop() -> int:
    while True:
        letters = input('> ').lower()
        if letters == '_ex':
            return 0  # exits
        elif letters in ('help', '?'):  # x == y or x == z
            println(
                "usage: <included_letters>[/<required_letters>]",
                "included letters may be in the words, required letters must be in the words",
                "",
                "type '_ex' to exit",
                sep='\n',
            )
            continue
        else:
            # run main func
            find_words(letters)


if __name__ == '__main__':
    exit(mainloop())  # run the program
