#! /usr/bin/python3
# wux.py
# Charles Emerson
# Created: 29 Dec 2018
# Updated: 11 Mar 2019
#
# Run as a script, determines and records the current web novel
# book, chapter, and part of the entries web novels in "config.txt".
#
# Exercise in web crawling.

import requests

########################################################################
# HELPER FUNCTIONS
########################################################################

def extractAddr(fLine):
	"""Extract the formatted address and book, chapter, and part."""

	tokens = fLine.split()

	fAddr = tokens[0]
	count = fAddr.count('@')

	sections = [1] * count

	if len(tokens) >= count + 1:
		for i in range(0, count):
			sections[i] = int(tokens[i+1])

	return fAddr, sections


def formatAddr(fAddr, sections):
	"""Return the corresponding address with book, chapter and part."""
	output = fAddr

	for i in range(0, len(sections)):
		output = output.replace('@', str(sections[i]), 1)

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


########################################################################
# PRIMARY FUNCTION
########################################################################

def determineCurrentFrom(fAddr, sections):
	"""Determine the current book, chapter, part."""
	countUp = True

	state = 0
	stride = 1

	current = [1] * len(sections)

	numHttpRequests = 0
	while state < len(sections):

		current[state] = sections[state] + stride

		if stride == 0:
			state = state + 1
			countUp = True
			stride = 1
			continue


		addr = formatAddr(fAddr, current)
		numHttpRequests = numHttpRequests + 1
		if isGoodAddr(addr):
			sections = current.copy()

			if countUp:
				stride = 2 * stride
			else:
				stride = int(stride / 2)
		else:
			countUp = False
			stride = int(stride / 2)

	print('Total number of HTTP requests: ' + str(numHttpRequests))

	return sections


########################################################################
# MAIN
########################################################################

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

		fAddr, sections = extractAddr(line)

		print('Given: ' + formatAddr(fAddr, sections))
		sections = determineCurrentFrom(fAddr, sections)
		print('Current: ' + formatAddr(fAddr, sections))
		print()

		output = output + "\n" + fAddr

		for section in sections:
			output = output + " " + str(section)

	file = open('config.txt', "w")
	file.write(output)