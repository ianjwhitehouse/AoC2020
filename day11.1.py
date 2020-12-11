# Common Inputs
import string;
import os;
import copy;


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

# Main Method
# Load File
sampleText = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL""".split("\n")
with open("day11.txt") as f:
	fInput = [sampleText, f.readlines()];

# Main method
for text in fInput:
	# Uncomment for debugger
	# db = DebugFile();
	# db.line(); #Put this inside the main loop to add lines to the debug file

	answer = 100;
	# END OF PREDEFINED
	seats = [];
	for line in text:
		seats.append([letter for letter in line.strip()]);
	rRange = len(seats);
	cRange = len(seats[0]);
	finalSeats = {};
	for rIndex in range(len(seats)):
		for cIndex in range(len(seats[rIndex])):
			finalSeats[(rIndex, cIndex)] = seats[rIndex][cIndex];
	seats = finalSeats;

	change = 100;
	while change != 0:
		newSeats = copy.deepcopy(seats);
		lastAnswer = answer;
		for rIndex in range(rRange):
			for cIndex in range(cRange):
				if seats[(rIndex, cIndex)] == "L":
					success = True;
					for rOff in range(-1, 2):
						for cOff in range(-1, 2):
							try:
								if seats[(rIndex + rOff, cIndex + cOff)] == "#":
									success = False;
							except:
								pass;
					if success:
						newSeats[(rIndex, cIndex)] = "#";
				elif seats[(rIndex, cIndex)] == "#":
					success = 0;
					for rOff in range(-1, 2):
						for cOff in range(-1, 2):
							try:
								if seats[(rIndex + rOff, cIndex + cOff)] == "#":
									success += 1;
							except:
								continue;
					if success >= 5:
						newSeats[(rIndex, cIndex)] = "L";
		answer = 0;
		allSeats = []
		for rIndex in range(rRange):
			for cIndex in range(cRange):
				#print(newSeats[(rIndex, cIndex)], end="");
				allSeats.append(newSeats[(rIndex, cIndex)]);
			#print("", end="\n");

		answer = allSeats.count("#");
		#print("");
		change = lastAnswer - answer;
		seats = newSeats;

	# BEGINNING OF PREDEFINED
	print(answer);

	# Uncomment for debugger
	# print("Saved at %s" % db.startingFile);
	# del db;

# Return answer
os.system('echo ' + str(answer).strip() + '| clip');