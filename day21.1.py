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



# Main Method
# Load File
sampleText = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)""".split("\n")
with open("day21.txt") as f:
	fInput = [sampleText, f.readlines()];

# Main method
for text in fInput:
	# Uncomment for debugger
	# db = DebugFile();
	# db.line(); #Put this inside the main loop to add lines to the debug file

	answer = 0;
	# END OF PREDEFINED
	allIng = [];
	allergens = [];

	for line in text:
		line = line.strip();
		line = line.split(" (contains ");
		allIng.append(line[0].split(" "));
		allergens.append(line[1][:-1].split(", "));

	allAle = {};
	for ing, ale in zip(allIng, allergens):
		for al in ale:
			if al in allAle.keys():
				allAle[al].append(ing);
			else:
				allAle[al] = [ing];
	allergens = allAle;

	nAllergens = {};
	for key, item in allergens.items():
		posAl = [];
		for i in item:
			for ii in i:
				posAl.append(ii);
		posAl = list(dict.fromkeys(posAl));
		for i in posAl:
			if all(i in val for val in item):
				if key in nAllergens.keys():
					nAllergens[key].append(i);
				else:
					nAllergens[key] = [i];

	allIng = flatten(allIng);
	nIngs = [];
	for ing in list(dict.fromkeys(allIng)):
		if all([ing not in val for val in nAllergens.values()]):
			nIngs.append(ing);

	for ing in nIngs:
		answer += allIng.count(ing);

	# BEGINNING OF PREDEFINED
	print(answer);

	# Uncomment for debugger
	# print("Saved at %s" % db.startingFile);
	# del db;

# Return answer
os.system('echo ' + str(answer).strip() + '| clip');