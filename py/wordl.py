#!/usr/bin/env python
# very bad wordle solver thing

import json, os, re, random
from colorama import Fore, Style
from typing import Tuple, List, Union


def colorize(string: str, ansi: str) -> str:
	return f"{ansi}{string}{Style.RESET_ALL}"


def setup(path: str = "words") -> Tuple[int, List[str]]:
	print("loading...", end="")

	if os.path.exists(path):
		with open(path, "r") as file:
			orig_target = json.loads(file.read())
	else:
		return 1, []

	print("done")
	print("\033[4mCANNOT always handle double letters\033[0m")  # idk
	return 0, orig_target


def reset() -> None:
	global include, exclude, positional_exclude  # fine
	include = set()
	exclude = set()
	positional_exclude = []
	print("resetting...")


def norepeat(
	orig_target: List[str], length: int = 0, limit: Union[int, None] = 10
) -> None:
	if not length or not 3 < length < 12:
		print(
			"usage: words <length> [limit]\n"
			"example: words 5 5\n"
			"length can be from 4-11, limit is 10 by default"
		)
		return

	if limit == -1:
		limit = None

	out = []
	trimmed = [word for word in orig_target if len(word) == length]
	random.shuffle(trimmed)  # return new words

	for word in trimmed:
		match = re.search(r"(.).*\1", word)
		if not match:
			out += [word]

	print(*out[:limit], sep=", ")


def solve(orig_target: List[str], w: str) -> None:
	w = [*map(str.strip, w.split(","))]
	if not all(c in "gyb" for c in w[1]) or len(w[1]) != len(w[0]):
		print("bad word/pattern")
		return

	stat_zip = [*zip(w[0], w[1])]
	for t in stat_zip:
		if t[1] in "yg" and t[0] not in include:
			print(f"{colorize('including', Fore.LIGHTGREEN_EX)} {t[0]}")
			include.add(t[0])

		elif t[1] == "b" and t[0] not in include and t[0] not in exclude:
			print(f"{colorize('excluding', Fore.LIGHTRED_EX)} {t[0]}")
			exclude.add(t[0])

	# same length
	target = [
		word
		for word in orig_target
		if len(word) == len(w[0]) and word not in positional_exclude
	]

	# include/exclude
	include_list = [word for word in target if all(char in word for char in include)]
	exclude_list = [word for word in target if any(char in word for char in exclude)]

	# positional (maybe works)
	inter = [word for word in include_list if word not in exclude_list]

	for word in inter:
		for idx, char in enumerate(word):
			if w[1][idx] == "g":  # good letter
				if not w[0][idx] == char:  # letter DOESN'T match
					print(
						f"{colorize('excluding', Fore.LIGHTRED_EX)} {word} ({colorize('green', Fore.LIGHTGREEN_EX)} mismatch)"
					)
					positional_exclude.append(word)
					break

			if w[1][idx] == "y":  # maybe letter
				if w[0][idx] == char:  # letter DOES match
					print(
						f"{colorize('excluding', Fore.LIGHTRED_EX)} {word} ({colorize('yellow', Fore.LIGHTYELLOW_EX)} mismatch)"
					)
					positional_exclude.append(word)
					break

	good_list = [word for word in inter if word not in positional_exclude]
	if len(good_list) == 0:
		print("no words found, maybe you made a typo?")
		return reset()
	print(*good_list, sep=", ")


def main() -> int:
	status, target = setup()
	if status != 0:
		print("wordlist not found")
		return status

	while True:
		try:
			w = input("> ")  # word,status
		except (KeyboardInterrupt, EOFError):
			return 0

		match w:
			case "reset":
				reset()
			case "include":
				print(*include, sep=", ")
			case "exclude":
				print(*exclude, sep=", ")
			case "?" | "help":
				print(
					"usage: <word>,<pattern> (black/yellow/green)\n"
					"example: world,byybg\n\n"
					"ctrl-c to exit"
				)
			case _ if "," not in w:
				if w.startswith("words"):
					w = map(int, w.split()[1:])
					norepeat(target, *w)
				else:
					print("invalid command (words, include, exclude, reset, help)")
			case _:
				solve(target, w)


if __name__ == "__main__":
	include = set()
	exclude = set()
	positional_exclude = []

	exit(main())
