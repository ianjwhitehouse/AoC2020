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
def countNeighbor(grid, x, y, z, w):
	coun = 0;
	for nX in range(x-1, x + 2):
		for nY in range(y - 1, y + 2):
			for nZ in range(z - 1, z + 2):
				for nW in range(w - 1, w + 2):
					if grid[nX][nY][nZ][nW]:
						coun += 1;
	if grid[x][y][z][w]:
		coun -= 1;
	return coun;


# Main Method
# Load File
sampleText = """.#.
..#
###""".split("\n");
with open("day17.txt") as f:
	fInput = [sampleText, f.readlines()];

# Main method
for text in fInput:
	# Uncomment for debugger
	# db = DebugFile();
	# db.line(); #Put this inside the main loop to add lines to the debug file

	answer = 0;
	# END OF PREDEFINED

	size = 30;
	offset = size //2 - 1;

	grid = [[[[False for m in range(size)] for k in range(size)] for j in range(size)] for i in range(size)];

	for y in range(len(text)):
		for x in range(len(text[y])):
			grid[x+offset][y+offset][offset][offset] = text[y][x] == "#";
	print(flatten(grid).count(True));

	for i in range(6):
		nGrid = [[[[False for x in range(size)] for y in range(size)] for z in range(size)] for w in range(size)];
		for x in range(1, size-1):
			for y in range(1, size-1):
				for z in range(1, size-1):
					for w in range(1, size-1):
						active = grid[x][y][z][w];
						if active and (countNeighbor(grid, x, y, z, w) == 2 or countNeighbor(grid, x, y, z, w) == 3):
							nGrid[x][y][z][w] = True;
						elif not active and countNeighbor(grid, x, y, z, w) == 3:
							nGrid[x][y][z][w] = True;
		grid = nGrid
		answer = 0
		for x in range(1, size - 1):
			for y in range(1, size - 1):
				for z in range(1, size - 1):
					for w in range(1, size - 1):
						if grid[x][y][z][w]:
							answer += 1;
		print(answer);
		print();


	# BEGINNING OF PREDEFINED
	print(answer);

	# Uncomment for debugger
	# print("Saved at %s" % db.startingFile);
	# del db;

# Return answer
os.system('echo ' + str(answer).strip() + '| clip');