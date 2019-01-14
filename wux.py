#! /usr/bin/python3
# findCurrentWebNovelChapter.py
# Charles Emerson
# Created: 29 Dec 2018
# Updated: 14 Jan 2019
#
# Run as a script, determines and records the current web novel
# book, chapter, and part of the entries web novels in "config.txt".
#
# Exercise in web crawling.

import requests

########################################################################

def extractAddr(fLine):
	"""Extract the formatted address and book, chapter, and part."""

	tokens = fLine.split()

	book = None
	chapter = None
	part = None

	fAddr = tokens[0]
	i = 1
	if '@' in fAddr:
		book = int(tokens[i])
		i += 1
	if '%' in fAddr:
		chapter = int(tokens[i])
		i += 1
	if '!' in fAddr:
		part = int(tokens[i])

	return fAddr, book, chapter, part


def formatAddr(fAddr, book, chapter, part):
	"""Return the corresponding address with book, chapter and part."""
	output = fAddr

	if '@' in fAddr and book:
		output = output.replace('@', str(book))

	if '%' in fAddr and chapter:
		output = output.replace('%', str(chapter))

	if '!' in fAddr and part:
		output = output.replace('!', str(part))

	return output

def isGoodContent(content):
	"""Returns whether not a Teaser and not past the latest chapter."""
	verboten = [
		"You\\'ve caught up with the latest released chapter.",
		"(Teaser)",
	]
	for phrase in verboten:
		if phrase in content:
			return False
	return True

def isGoodStatus(status_code):
	"""Returns true if "Success" HTML status code."""
	# 1: "Info"
	# 2: "Success"
	# 3: "Redirect"
	# 4: "Client Error"
	# 5: "Server Error"
	return int(status_code/100) == 2

def isGoodAddr(addr):
	"""Returns true if a request was successful and had good content."""
	response = requests.get(addr)
	return isGoodStatus(response.status_code) \
		and isGoodContent(str(response.content))

def findBCP(fAddr, book, chapter, part):
	"""Determine the current book, chapter, part."""
	countUp = True

	STATE = 3
	stride = 1

	b = None
	c = None
	p = None

	i = 0
	while STATE > 0:

		if (STATE == 3 and not book) or \
		   (STATE == 2 and not chapter) or \
		   (STATE == 1 and not part) or \
		   stride == 0:

			STATE = STATE - 1
			stride = 1
			failed = False
			countUp = True
			continue


		if STATE == 3:
			b = book + stride
			c = 1
		if STATE == 2:
			c = chapter + stride
		if STATE == 1:
			p = part + stride
		elif part:
			p = 1

		i = i + 1
		addr = formatAddr(fAddr, b, c, p)

		if isGoodAddr(addr):
			book = b
			chapter = c
			part = p

			if countUp:
				stride = 2 * stride
			elif failed:
				stride = int(stride / 2)
				# failed = False
		else:
			countUp = False
			stride = int(stride / 2)
			failed = True

	print('# of iterations: ' + str(i))

	return book, chapter, part

####################################################

if __name__ == "__main__":
    # execute only if run as a script
	file = open('config.txt', "r")
	input = file.read().split("\n")
	output = ""

	for line in input:
		if not line or '#' in line:
			if output:
				output = output + "\n" + line
			else:
				output = line
			continue

		fAddr, book, chapter, part = extractAddr(line)

		print('Given: book ' + str(book) + ', chapter ' + str(chapter) + ', part ' + str(part))
		book, chapter, part = findBCP(fAddr, book, chapter, part)
		print('Output: book ' + str(book) + ', chapter ' + str(chapter) + ', part ' + str(part))
		print('Visit \"' + formatAddr(fAddr, book, chapter, part) + '\"')
		print()

		output = output + "\n" + fAddr
		if book:
			output = output + " " + str(book)
		if chapter:
			output = output + " " + str(chapter)
		if part:
			output = output + " " + str(part)

	file = open('config.txt', "w")
	file.write(output)