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
class Tile:
	def __init__(self):
		self.val = True;
		self.e = None;
		self.se = None;
		self.sw = None;
		self.w = None;
		self.nw = None;
		self.ne = None;

	def count(self):
		cnt = 0;
		try:
			if not self.e.val:
				cnt += 1;
		except:
			# return False;
			pass;
		try:
			if not self.se.val:
				cnt += 1;
		except:
			# return False;
			pass;
		try:
			if not self.sw.val:
				cnt += 1;
		except:
			# return False;
			pass;
		try:
			if not self.w.val:
				cnt += 1;
		except:
			# return False;
			pass;
		try:
			if not self.nw.val:
				cnt += 1;
		except:
			# return False;
			pass;
		try:
			if not self.ne.val:
				cnt += 1;
		except:
			# return False;
			pass;
		return cnt;


def genTiles(w, h):
	wholeFloor = [];
	for y in range(-h, h):
		row = [];
		lastTile = None;
		if y % 2 == 0:
			for x in range(-w, w):
				if lastTile is not None:
					lastTile.e = Tile();
					lastTile.e.w = lastTile;
					row.append(lastTile.e);
					lastTile = lastTile.e;
				else:
					lastTile = Tile();
		else:
			for x in range(-w, w - 1):
				if lastTile is not None:
					lastTile.e = Tile();
					lastTile.e.w = lastTile;
					row.append(lastTile.e);
					lastTile = lastTile.e;
				else:
					lastTile = Tile();
		if len(wholeFloor) > 0:
			lastRow = wholeFloor[-1];
			if len(row) > len(lastRow):
				for tile in row[:-1]:
					tile.se = lastRow[row.index(tile)];
					tile.se.nw = tile;
					tile.se.ne = row[row.index(tile) + 1];
					tile.se.ne.sw = tile.se;
			else:
				for tile in row:
					tile.sw = lastRow[row.index(tile)];
					tile.sw.ne = tile;
					tile.se = lastRow[row.index(tile) + 1];
					tile.se.nw = tile;
		wholeFloor.append(row);
	return wholeFloor, wholeFloor[h][w];


# Main Method
# Load File
sampleText = """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew""".split("\n")
with open("day24.txt") as f:
	fInput = [sampleText, f.readlines()];

# Main method
for text in fInput:
	# Uncomment for debugger
	# db = DebugFile();
	# db.line(); #Put this inside the main loop to add lines to the debug file

	answer = 0;
	# END OF PREDEFINED

	tiles, startTile = genTiles(200, 200);
	flips = [];
	for line in text:
		line = line.strip();
		thisStartTile = startTile;
		while len(line) > 0:
			if line.startswith("se"):
				line = line[2:];
				thisStartTile = thisStartTile.se;
			elif line.startswith("sw"):
				line = line[2:];
				thisStartTile = thisStartTile.sw;
			elif line.startswith("nw"):
				line = line[2:];
				thisStartTile = thisStartTile.nw;
			elif line.startswith("ne"):
				line = line[2:];
				thisStartTile = thisStartTile.ne;
			elif line.startswith("w"):
				line = line[1:];
				thisStartTile = thisStartTile.w;
			elif line.startswith("e"):
				line = line[1:];
				thisStartTile = thisStartTile.e;
		flips.append(thisStartTile.val);
		thisStartTile.val = not thisStartTile.val;

	nTiles = flatten(tiles);
	for i in range(1, 101):
		tilesToFlip = [];
		for tile in nTiles:
			if tile.val:
				if tile.count() == 2:
					# if not (tile.count() == False):
					tilesToFlip.append(tile);
			else:
				if tile.count() == 0 or tile.count() > 2:
					# if not (tile.count() == False):
					tilesToFlip.append(tile);
		for tile in tilesToFlip:
			tile.val = not tile.val;
		nTiles = flatten(tiles);
		answer = [tile.val for tile in nTiles].count(False);
		print(i, answer)

	# BEGINNING OF PREDEFINED
	print(answer);

	# Uncomment for debugger
	# print("Saved at %s" % db.startingFile);
	# del db;

# Return answer
os.system('echo ' + str(answer).strip() + '| clip');