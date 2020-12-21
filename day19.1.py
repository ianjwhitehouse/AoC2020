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
def combineAddTwo(x, y):
	all = [];
	for xV in x:
		for yV in y:
			all.append(xV+yV);
	return all;

def combineAdd(vals=[]):
	all = [""];
	for v in vals:
		all = combineAddTwo(all, v);
	return all;


def genOptionsForRule(rule, rules):
	rule = rules[rule]
	if type(rule) == type(""):
		return [rule];
	elif type(rule[0]) == type([]):
		all = [];
		for rs in rule:
			all += combineAdd([genOptionsForRule(r, rules) for r in rs]);
		return all;
	elif type(rule[0]) == type(int("1")):
		return combineAdd([genOptionsForRule(r, rules) for r in rule]);


def proccessMessage(message, rule, rules):
	if type(rules[rule]) == type(""):
		return message[0] == rules[rule], 1;
	elif type(rules[rule][0]) == type([]):
		retVals = [];
		sizes = [];
		for rs in rules[rule]:
			reVal = True;
			i = 0;
			for r in rs:
				try:
					rreVal, size = proccessMessage(message[i:], r, rules);
				except:
					rreVal = False;
					size = 1;
				reVal = reVal and rreVal;
				i += size;
				sizes.append(size);
			retVals.append(reVal);
		return any(retVals), sum(sizes)//2;
	elif type(rules[rule][0]) == type(int("1")):
		retVals = [];
		i = 0;
		for rs in rules[rule]:
			ret, size = proccessMessage(message[i:], rs, rules);
			retVals.append(ret);
			i += size;
		return all(retVals), i;


# Main Method
# Load File
sampleText = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb""".split("\n")
with open("day19.txt") as f:
	fInput = [sampleText, f.readlines()];

# Main method
for text in fInput:
	# Uncomment for debugger
	# db = DebugFile();
	# db.line(); #Put this inside the main loop to add lines to the debug file

	answer = 0;
	# END OF PREDEFINED
	text = [l.strip() for l in text];
	rules = {};
	for line in text[:text.index("")]:
		l = line.split(": ");
		if l[1].startswith('"'):
			rules[int(l[0])] = l[1][1:2];
		else:
			rule = [];
			for i in l[1].split(" "):
				if i == "|":
					rules[int(l[0])] = rule;
					rule = [];
				else:
					rule.append(int(i));

			try:
				rules[int(l[0])]
				rules[int(l[0])] = [rules[int(l[0])], rule];
			except:
				rules[int(l[0])] = rule;

	# Process messages
	for message in text[text.index("") + 1:]:
		chk = proccessMessage(message, 0, rules);
		if chk[0] and chk[1] == len(message):
			answer += 1;


	# BEGINNING OF PREDEFINED
	print(answer);

	# Uncomment for debugger
	# print("Saved at %s" % db.startingFile);
	# del db;

# Return answer
os.system('echo ' + str(answer).strip() + '| clip');