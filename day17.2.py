# Common Inputs
import string;
import os;
from numpy import prod;
from copy import copy, deepcopy;
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
def countSurround(cubes, key):
	cs = 0;
	for x in range(key[0] - 1, key[0] + 2):
		for y in range(key[1] - 1, key[1] + 2):
			for z in range(key[2] - 1, key[2] + 2):
				for w in range(key[3] - 1, key[3] + 2):
					if (x, y, z, w) != key:
						try:
							if cubes[(x, y, z, w)]:
								cs += 1;
						except:
							pass;
	return cs;


def fancyPrint(cubes, xMin, xMax, yMin, yMax, zMin, zMax, wMin, wMax, i):
	print("i: %s, x: %s - %s y: %s - %s z: %s - %s" %(i, xMin, xMax, yMin, yMax, zMin, zMax))
	for w in range(wMin, wMax + 1):
		print("W: %s" %w);
		for z in range(zMin, zMax + 1):
			print("Z: %s" %z);
			for y in range(yMin, yMax + 1):
				for x in range(xMin, xMax + 1):
					try:
						print("#" if cubes[(x, y, z, w)] else ".", end="");
					except:
						print(".", end="");
				print();
			print();
		print();
	print();

# Main Method
# Load File
sampleText = """.#.
..#
###""".split("\n")
with open("day17.txt") as f:
	fInput = [sampleText, f.readlines()];

# Main method



for text in fInput:
	# Uncomment for debugger
	# db = DebugFile();
	# db.line(); #Put this inside the main loop to add lines to the debug file

	answer = 0;
	# END OF PREDEFINED

	cubes = {};
	for x in range(-5, 10):
		for y in range(-5, 10):
			for z in range(-5, 10):
				for w in range(-5, 10):
					cubes[(x, y, z, w)] = False;

	for x in range(len(text)):
		for y in range(len(text[0].strip())):
			cubes[(x, y, 0, 0)] = text[y][x] == "#";
	answer = list(cubes.values()).count(True);

	xMin, xMax = [-1, 10];
	yMin, yMax = [-1, 10];
	zMin, zMax = [-5, 5];
	wMin, wMax = [-5, 5];
	for i in range(6):
		# fancyPrint(cubes, xMin, xMax, yMin, yMax, zMin, zMax, wMin, wMax, i);
		newCubes = deepcopy(cubes);
		for key in cubes.keys():
			xCheck = key[0] in range(xMin - 1, xMax + 2);
			yCheck = key[1] in range(yMin - 1, yMax + 2);
			zCheck = key[2] in range(zMin - 1, zMax + 2);
			wCheck = key[3] in range(wMin - 1, wMax + 2);
			if xCheck and yCheck and zCheck and wCheck:
				newCubes[key] = False;
				if cubes[key]:
					if countSurround(cubes, key) == 2 or countSurround(cubes, key) == 3:
						newCubes[key] = True;
				else:
					if countSurround(cubes, key) == 3:
						newCubes[key] = True;
		cubes = deepcopy(newCubes);
		answer = list(cubes.values()).count(True);

		allXs = [key[0] for key, val in cubes.items() if val];
		xMin = min(allXs);
		xMax = max(allXs);

		allYs = [key[1] for key, val in cubes.items() if val];
		yMin = min(allYs);
		yMax = max(allYs);

		allZs = [key[2] for key, val in cubes.items() if val];
		zMin = min(allZs);
		zMax = max(allZs);

		allWs = [key[3] for key, val in cubes.items() if val];
		wMin = min(allWs);
		wMax = max(allWs);

		for x in range(xMin - 3, xMax + 4):
			for y in range(yMin - 3, yMax + 4):
				for z in range(zMin - 3, zMax + 4):
					for w in range(wMin - 3, wMax + 4):
						try:
							cubes[(x, y, z, w)];
						except:
							cubes[(x, y, z, w)] = False;

	# BEGINNING OF PREDEFINED

	print(answer);

	# Uncomment for debugger
	# print("Saved at %s" % db.startingFile);
	# del db;

# Return answer
os.system('echo ' + str(answer).strip() + '| clip');