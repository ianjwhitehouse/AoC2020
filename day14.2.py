# Common Inputs
import string;
import os;
from itertools import chain;


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


def findPosVals(val, front=""):
	posibilities = [];
	if not "X" in val:
		return front + val;
	for i, v in enumerate(val):
		if v == "X":
			tempV = val;
			posibilities.append(findPosVals("1" + tempV[i + 1:], front=front + tempV[:i]));
			posibilities.append(findPosVals("0" + tempV[i + 1:], front=front + tempV[:i]));
			break;
	return posibilities;



def makeVal(val, mask):
	val = bin(val)[2:].zfill(36);
	finalVal = "";
	for p in zip(val, mask):
		if p[1] == "0":
			finalVal += p[0];
		else:
			finalVal += p[1];
	val = flatten(findPosVals(finalVal));
	return [int(v, 2) for v in val];


# Main Method
# Load File
sampleText = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1""".split("\n")
with open("day14.txt") as f:
	fInput = [sampleText, f.readlines()];

# Main method
for text in fInput:
	# Uncomment for debugger
	# db = DebugFile();
	# db.line(); #Put this inside the main loop to add lines to the debug file

	answer = 0;
	# END OF PREDEFINED
	mask = "";
	mem = {};

	for code in text:
		cmd = code.split(" = ")[0];
		val = code.split(" = ")[1];
		if cmd == "mask":
			mask = val.strip();
			print("Current mask combinations: %d" %pow(2, mask.count("X")));
		elif cmd.startswith("mem"):
			startingAd = int("".join(cmd.split("[")[1][:-1]));
			for addy in makeVal(startingAd, mask):
				mem[addy] = int(val.strip());
		print(round((text.index(code)/len(text)) * 100, 2));

	answer = sum(mem.values());


	# BEGINNING OF PREDEFINED
	print(answer);

	# Uncomment for debugger
	# print("Saved at %s" % db.startingFile);
	# del db;

# Return answer
os.system('echo ' + str(answer).strip() + '| clip');