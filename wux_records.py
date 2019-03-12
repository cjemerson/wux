#! /usr/bin/python3
# wux_records.py
# Charles Emerson
# Created: 11 Mar 2019
# Updated: 11 Mar 2019
#
# Run as a script, manages Records of the current web novel chapters.
# Stores these Records in "wux_save.txt"
#
# Exercise in web crawling.


#######################################################################
# To open a new web page (MODIFY THIS)
#######################################################################
import os
import subprocess

def openWebPage(htmlAddress):
	FNULL = open(os.devnull, 'w')
	retcode = subprocess.Popen(['vivaldi.exe', htmlAddress], stdout=FNULL, stderr=subprocess.STDOUT)


#######################################################################
# Modules
#######################################################################
import os.path
from wux import *


#######################################################################
# Record class
#######################################################################
class Record(object):
	def __init__(self, fAddr, sections):
		self.fAddr = fAddr
		self.sections = sections

	def getAddress(self):
		return formatAddr(self.fAddr, self.sections)

	def getNumSections(self):
		return len(self.sections)

	def setSections(self, sections):
		self.sections = sections

	def getRaw(self):
		return self.fAddr, self.sections

	def formatWith(self, sections):
		return formatAddr(self.fAddr, sections)

	def findNext(self, num):
		if num <= 0:
			return []
		addrList = []

		end = len(self.sections) - 1

		index = end
		failed = True

		current = self.sections.copy()

		while True:
			current[index] += 1

			addr = self.formatWith(current)
			if isGoodAddr(addr):
				addrList.append(addr)
				if len(addrList) == num:
					break;

				if failed:
					index = end
				failed = False
			elif index == 0:
				break;
			else:
				failed = True
				current[index:] = [1] * len(current[index:])
				index -= 1

		return addrList

	def isValid(self):
		return isGoodAddr(self.getAddress())


#######################################################################
# FILE OPERATIONS
#######################################################################

# Opens the save file and parses it for the records
def parseForRecords(filename):
	records = {}

	if not os.path.isfile("./" + filename):
		return records

	file = open(filename, "r")
	input = file.read().split("\n")

	for line in input:
		if not line:
			break;
		spacePos = line.find(' ')
		alias = line[0:spacePos]
		fAddr, sections = extractAddr(line[spacePos+1:])
		records[alias] = Record(fAddr, sections)

	return records

def storeRecordsAt(filename, records):
	file = open(filename, "w")

	output = ""
	for alias, record in records.items():
		fAddr, sections = record.getRaw()
		output += alias + " " + fAddr + " "
		output += " ".join([str(x) for x in sections]) + "\n"

	file.write(output)


#######################################################################
# COMMAND HANDLER FUNCTIONS
#######################################################################
def handle_read(records, args):
	if len(args) != 3 or args[1] not in records:
		print("Usage: \"read <alias> <number to open>\"")
		print("Alternate: \"read <alias> all\" (Hardcoded 10 max)")
		return

	numToOpen = 10
	if args[2] != "all":
		numToOpen = int(args[2])

		if numToOpen <= 0:
			print("Invalid number to open")
			return

	record = records[args[1]]
	addresses = record.findNext(numToOpen);

	for addr in addresses:
		print(addr)
		openWebPage(addr)

def handle_list(records, args):
	if len(args) > 1 and args[1] in records:
		alias = args[1]
		print("\t" + alias + ": " + records[alias].getAddress())
		return
	for alias, record in records.items():
		print("\t" + alias + ": " + record.getAddress())

def handle_add(records, args):
	if len(args) < 3:
		print("Usage: \"add <alias> <formatted_address> <section numbers>\"")
		return

	alias = args[1]
	if alias in records:
		print("Alias already exists in Records")
		return

	fAddr = args[2]
	count = fAddr.count('@')

	if count == 0:
		print("Invalid formatted address input.")
		return

	if len(args) != count + 3:
		print("Invalid number of sections input")
		return

	record = Record(fAddr, [1] * count)

	sections = [int(x) for x in args[3:]]
	if sum(1 for x in sections if x < 0) != 0:
		print("Invalid sections input")
		return

	record.setSections(sections)
	if record.isValid():
		records[alias] = record
	else:
		print("Invalid Record")

def handle_remove(records, args):
	if len(args) != 2 or args[1] not in records:
		print("Usage: \"remove <alias>\"")
		return

	alias = args[1]

	doublecheck = input("To remove the Record, type \"" + alias + "\": ")
	if doublecheck == alias:
		del records[alias]

def handle_update(records, args):
	if (len(args) < 2 or args[1] not in records):
		print("Usage: \"update <alias> <section numbers>")
		return

	alias = args[1]
	if (len(args) != 2 + records[alias].getNumSections()):
		print("Invalid number of sections provided")
		return

	if alias in records:
		sections = [int(x) for x in args[2:]]
		if sum(1 for x in sections if x < 0) == 0:
			records[alias].setSections(sections)
		else:
			print("Invalid sections")

def handle_current(records, args):
	if len(args) != 2:
		print("Usage: \"current <alias>\"")
		return

	alias = args[1]
	fAddr, sections = records[alias].getRaw()
	sections = determineCurrentFrom(fAddr, sections)
	print(records[alias].formatWith(sections))


#######################################################################
# MAIN
#######################################################################
if __name__ == "__main__":
	records = parseForRecords("wux_save.txt")

	ws = " " * 4
	while (True):
		userline = input(">> wux >> ")

		args = userline.split()
		if len(args) == 0:
			print("For usage type in \"help\"")
		elif (args[0] == "list"):
			handle_list(records, args)
		elif (args[0] == "read"):
			handle_read(records, args)
		elif (args[0] == "add"):
			handle_add(records, args)
		elif (args[0] == "update"):
			handle_update(records, args)
		elif (args[0] == "exit"):
			break;
		elif (args[0] == "current"):
			handle_current(records, args)
		elif (args[0] == "remove"):
			handle_remove(records, args)
		elif (args[0] == "help"):
			print("\nVALID COMMANDS:")
			print("list - List the Records")
			print("read - Open a Record")
			print("add - Add a Record")
			print("remove - Remove a Record")
			print("update - Manually update a Record")
			print("exit - Exit the program")
			print("current - Determine the most recent post")
			print("help - Print this message")
		else:
			print("For usage type in \"help\"")

		print()

	storeRecordsAt("wux_save.txt", records)
