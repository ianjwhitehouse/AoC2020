# Common Inputs
import string;
import os;
from numpy import prod;
from copy import deepcopy;
from math import cos, sin, degrees, radians, gcd;
from numpy import prod;



# Classes and functions
class VM:
	def __init__(self, beginingLine=0, beginingValue=0):
		self.curLine = beginingLine;
		self.val = beginingValue;

	def __repr__(self):
		return str("Line Number %s, value %s" %(self.curLine, self.val));

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
				self.file = open("debug%s.txt" %startingFile, "x");
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
			if sum(lst[i:i+rangeSize]) == sSum:
				return lst[i:i+rangeSize];
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
class cup:
	def __init__(self, val):
		self.val = val;
		self.n = None;
		self.p = None;


# Main Method
# Load File
sampleText = """389125467""";
with open("day23.txt") as f:
	fInput = [sampleText, f.read()];

# Main method
for text in fInput:
	# Uncomment for debugger
	# db = DebugFile();
	# db.line(); #Put this inside the main loop to add lines to the debug file

	answer = 1;
	# END OF PREDEFINED

	cups = [int(i) for i in text];
	nCups = {};
	prev = None
	for cu in cups:
		c = cup(cu);
		nCups[cu] = c;
		if prev != None:
			prev.n = c;
			c.p = prev;
		prev = c;

	mx = max(cups)
	for i in range(mx+1, 1_000_001):
		c = cup(i);
		nCups[i] = c;
		if prev != None:
			prev.n = c;
			c.p = prev;
		prev = c;
	prev.n = nCups[cups[0]];
	nCups[cups[0]].p = prev;

	star = cups[0];
	cups = nCups;
	curCup = cups[star];
	for actions in range(10_000_000):
		pickUpCups = [curCup.n];
		pickUpCups.append(pickUpCups[-1].n);
		pickUpCups.append(pickUpCups[-1].n);
		curCup.n = pickUpCups[-1].n;
		curCup.n.p = curCup;

		desCup = curCup.val - 1;
		while desCup in [c.val for c in pickUpCups + [cup(0)]]:
			desCup -= 1;
			if desCup <= 0:
				desCup = 1_000_000;
		desCup = cups[desCup];

		pickUpCups[-1].n = desCup.n;
		pickUpCups[-1].n.p = pickUpCups[-1];
		desCup.n = pickUpCups[0];
		desCup.n.p = desCup;

		curCup = curCup.n;
		answer = cups[1].n.val * cups[1].n.n.val;

	# BEGINNING OF PREDEFINED
	print(answer);

	# Uncomment for debugger
	# print("Saved at %s" % db.startingFile);
	# del db;

# Return answer
os.system('echo ' + str(answer).strip() + '| clip');