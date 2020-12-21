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
def solve(lst):
	fNum = None;
	op = "";
	for iindex, i in enumerate(lst):
		if iindex % 2 == 1:
			op = i;
		elif iindex == 0:
			fNum = int(i);
		else:
			if op == "*":
				fNum *= int(i);
			else:
				fNum += int(i);
			op = "";
	return fNum if fNum != None else 0;


def nSolve(lst):
	while lst.count("*") + lst.count("+") > 0:
		nList = [];
		iSToSolve = [];
		for i in range(len(lst)):
			if lst[i] == "*" and lst.count("+") == 0:
				iSToSolve.append(i);
			elif lst[i] == "+":
				iSToSolve.append(i);

		allReadySolved = False;
		dontAdd = [];
		for i in range(len(lst)):
			if i + 1 in iSToSolve and not allReadySolved:
				if lst[i+1] == "+":
					nList.append(int(lst[i]) + int(lst[i+2]));
				else:
					nList.append(int(lst[i]) * int(lst[i + 2]));
				allReadySolved = True;
				dontAdd = [i, i+1, i+2];
			else:
				if i not in dontAdd:
					nList.append(lst[i]);
		lst = nList;
	return lst[0];


def solvePara(lst):
	toSolve =[];
	depth = -1;
	priorDepth = -1;
	for i, v in enumerate(lst):
		if v.startswith("("):
			depth += v.count("(");
		elif v.endswith(")"):
			depth -= v.count(")");

		if depth > 0 and priorDepth < 1:
			startIndex = i;
		elif depth < 1 and priorDepth > 0:
			nLst = [];
			if startIndex == 0:
				nLst.append(lst[startIndex][1:]);

			else:
				nLst.append(lst[startIndex]);

			nLst += lst[startIndex + 1:i];

			if i+1 == len(lst):
				nLst.append(lst[i][:-1]);

			else:
				nLst.append(lst[i]);

			toSolve.append(solvePara(nLst));
		elif depth < 1:
			toSolve.append(v.replace("(", "").replace(")", ""));

		priorDepth = depth;

		if depth == -1:
			break;
	return nSolve(toSolve);

# def addParasForAddi(lst):
# 	lst = lst[:];
# 	comped = [];
# 	for i, v in enumerate(lst):
# 		if i not in comped:
# 			if v == "+":
# 				fDepth = 0 + lst[i-1].count("(") - lst[i-1].count(")");
# 				sDepth = 0 + lst[i+1].count("(") - lst[i+1].count(")");
# 				if depth < 1:
# 					for ii in range(i-1, i-1 + len(lst[i-1:])):
# 						nV = lst[ii];
# 						depth += nV.count("(");
# 						depth -= nV.count(")");
# 						if depth == 0 and nV == "+":
# 							comped.append(ii);
# 						if depth == 0 and nV == "*":
# 							lst[i-1] = "(" + lst[i-1];
# 							lst[ii-1] = lst[ii-1] + ")";
# 							break;
# 						elif depth <= 0 and nV.endswith(")"):
# 							lst[i - 1] = "(" + lst[i - 1];
# 							lst[ii] = lst[ii] + ")";
# 							break;
# 				else:
# 					for ii in range(i-1, 0, -1):
# 						nV = lst[ii];
# 						depth += nV.count("(");
# 						depth -= nV.count(")");
# 						if depth >= 0 and nV.endswith("("):
# 							lst[ii] = "(" + lst[ii];
# 							lst[i + 1] = lst[i + 1] + ")";
# 							break;
#
# 	return lst;


# Main Method
# Load File
sampleText = """2 * 3 + (4 * 5)
5 + (8 * 3 + 9 + 3 * 4 * 3)
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2""".split("\n");
with open("day18.txt") as f:
	fInput = [sampleText, f.readlines()];

# Main method
for text in fInput:
	# Uncomment for debugger
	# db = DebugFile();
	# db.line(); #Put this inside the main loop to add lines to the debug file

	answer = 0;
	# END OF PREDEFINED
	for line in text:
		line = line.strip();
		vals = line.split(" ");
		vals[0] = "(" + vals[0];
		vals[-1] = vals[-1] + ")";
		answer += solvePara(vals);
		print(solvePara(vals));
		print("");


	# BEGINNING OF PREDEFINED
	print();
	print(answer);
	print();

	# Uncomment for debugger
	# print("Saved at %s" % db.startingFile);
	# del db;

# Return answer
os.system('echo ' + str(answer).strip() + '| clip');