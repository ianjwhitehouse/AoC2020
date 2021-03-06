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
def recCombat(players):
	allRounds = [];
	while all([len(card) > 0 for card in players.values()]):
		if players in allRounds:
			return 1, players;
		elif players[1][0] <= len(players[1][1:]) and players[2][0] <= len(players[2][1:]):
			allRounds.append({key: item[:] for key, item in players.items()});
			nPlayer1 = players[1][1:players[1][0]+1];
			nPlayer2 = players[2][1:players[2][0]+1];
			winner, c = recCombat({1:nPlayer1, 2:nPlayer2});
		else:
			allRounds.append({key: item[:] for key, item in players.items()});
			winner = 1 if players[1][0] > players[2][0] else 2;

		play1Card = players[1].pop(0);
		play2Card = players[2].pop(0);
		if winner == 1:
			players[1] += [play1Card, play2Card];
		else:
			players[2] += [play2Card, play1Card];
	return 1 if len(players[2]) == 0 else 2, players;


# Main Method
# Load File
sampleText = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
""".split("\n");
# sampleText = """Player 1:
# 43
# 19
#
# Player 2:
# 2
# 29
# 14
# """.split("\n");
with open("day22.txt") as f:
	fInput = [sampleText, f.readlines()];

# Main method
for text in fInput:
	# Uncomment for debugger
	# db = DebugFile();
	# db.line(); #Put this inside the main loop to add lines to the debug file

	answer = 0;
	# END OF PREDEFINED

	player = 0;
	players = {};
	cards = [];
	for line in text:
		line = line.strip();
		if line.startswith("Player"):
			player = int(line.split(" ")[1][:-1]);
		elif line == "":
			players[player] = cards;
			cards = [];
		else:
			cards.append(int(line));

	winner, players = recCombat(players);

	for val in players.values():
		if len(val) > 0:
			val.reverse();
			for i, v in enumerate(val):
				answer += ((i+1) * v);

	# BEGINNING OF PREDEFINED
	print(answer);

	# Uncomment for debugger
	# print("Saved at %s" % db.startingFile);
	# del db;

# Return answer
os.system('echo ' + str(answer).strip() + '| clip');