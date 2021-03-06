# Common Inputs
import string;
import os;
from numpy import prod;
from copy import deepcopy;
from math import cos, sin, degrees, radians, gcd, prod;


# Classes and functions
class VM:
	def __init__(self, beginingLine=0, beginingValue=0):
		self.curLine = beginingLine;
		self.val = beginingValue;

	def __repr__(self):
		return str("Line Number %s, value %s" % (self.curLine, self.val));

	def getInt(self, line):
		"""
		Line should be a string with just the int part!
		:param line: string
		:return: int value
		"""
		if line.startswith("+"):
			return int(line[1:]);
		else:
			return int(line[1:]);

	def runLine(self, line):
		"""
		Line should be the full line, without the newline character!
		Make sure to edit the GOTO, SPLITTER and VALUE_ADDER values -- These were set based on 2020 day 8
		:param line: String
		:return: bool if it did something
		"""

		GOTO = "jmp";
		SPLITTER = " ";
		VALUE_ADDER = "acc";

		if line.split(SPLITTER)[0] == VALUE_ADDER:
			self.val += self.getInt(line.split(SPLITTER)[1])
			self.curLine;
			return True;

		elif line.split(SPLITTER)[0] == GOTO:
			if line.split(" ")[1].startswith("+"):
				self.curLine += int(line.split(" ")[1][1:]);
			else:
				self.curLine -= int(line.split(" ")[1][1:]);
			return True;

		self.curLine += 1;
		return False;

	def runLines(self, lines, ranLimit=100, pState=False):
		"""
		Run a list of lines, with or without newline characters.  Lines are just fed into the runLine one at a time
		:param lines: list of lines
		:param ranLimit: number of times a line can be ran before error
		:return: value
		"""
		ran = []
		while self.curLine < len(lines):
			ran.append(self.curLine);
			if ran.count(self.curLine) > ranLimit:
				print("Exceeded run limit")
				return 0;

			if lines[self.curLine].endswith("\n"):
				line = lines[self.curLine][:-1];
			else:
				line = lines[self.curLine]

			self.runLine(line);
			if pState:
				print(self);

		return self.val;


class DebugFile:
	def __init__(self):
		self.lines = [];
		startingFile = 0;
		while True:
			try:
				self.file = open("debug%s.txt" % startingFile, "x");
				self.startingFile = startingFile;
				self.file = open("debug%s.txt" % startingFile, "w");
				break;
			except:
				startingFile += 1;

	def line(self, line):
		line = str(line);
		self.lines.append(line);
		self.file.write(line + "\n");

	def __del__(self):
		self.file.close();


def getTwoNumbsThatSum(lst, sSum):
	for a in lst:
		for b in lst:
			if a + b == sSum:
				return [a, b];
	return False;


def getRangeOfNumbsThatSum(lst, sSum, max=100):
	rangeSize = 0;
	while rangeSize < max:
		for i in range(len(lst)):
			if sum(lst[i:i + rangeSize]) == sSum:
				return lst[i:i + rangeSize];
		rangeSize += 1;
	return False;


def flatten(lst):
	flatList = []
	if type(lst) == list:
		for i in range(len(lst)):
			flatList += flatten(lst[i]);
	else:
		flatList.append(lst);
	return flatList;


# END OF PREDEFINED FUNCTIONS


# Main Method
# Load File
sampleText = """class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9""".split("\n")
with open("day16.txt") as f:
	fInput = [sampleText, f.readlines()];

# Main method
for text in fInput:
	# Uncomment for debugger
	# db = DebugFile();
	# db.line(); #Put this inside the main loop to add lines to the debug file

	answer = 0;
	# END OF PREDEFINED

	# Parse
	curSection = 0;
	rules = {};
	# ticket = [val, val, val, val, val];
	myTicket = [];
	otherTickets = [];
	for line in text:
		if line.strip() == "":
			curSection += 1;
			pass;
		else:
			if curSection == 0:
				line = line.strip().split(": ");
				ranges = [];
				for r in line[1].split(" or "):
					ranges.append(range(int(r.split("-")[0]), int(r.split("-")[1]) + 1));
				rules[line[0]] = ranges;
			elif curSection == 1:
				if "your ticket:" not in line:
					myTicket = [int(x) for x in line.strip().split(",")];
			elif curSection == 2:
				if "nearby tickets" not in line:
					otherTickets.append([int(x) for x in line.strip().split(",")]);

	newTickets = deepcopy(otherTickets);
	for ticket in otherTickets:
		for val in ticket:
			if not any([val in r for r in flatten([rang for rang in rules.values()])]):
				newTickets.remove(ticket)

	cols = [];
	usedIs = [];
	while len(list(dict.fromkeys(usedIs))) < len(newTickets[0]):
		for i in range(len(newTickets[0])):
			if i not in usedIs:
				for name, ranges in rules.items():
					success = True;
					for ticket in newTickets:
						if not any([ticket[i] in r for r in ranges]):
							success = False;
							break;
					if success:
						cols.append((i, name));
		nCols = []
		for col in cols:
			if [c[1] for c in cols].count(col[1]) == 1:
				nCols.append(col);
				usedIs.append(col[0]);
		cols = nCols;


	lookForIndexes = [];
	for index, col in enumerate(cols):
		if col[1].startswith("departure"):
			lookForIndexes.append(col[0]);

	answer = prod([myTicket[i] for i in lookForIndexes]);

	# BEGINNING OF PREDEFINED
	print(answer);

# Uncomment for debugger
# print("Saved at %s" % db.startingFile);
# del db;

# Return answer
os.system('echo ' + str(answer).strip() + '| clip');