# Common Inputs
import string;
import os;
from numpy import prod;
from copy import deepcopy;
from math import cos, sin, degrees, radians, gcd, sqrt;
from numpy import prod;
import re;



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
class tileBasic:
	def __init__(self, tile, borders, key):
		self.tile = tile;
		self.borders = borders;
		self.key = key;

	def removeBorders(self):
		nTile = [];
		for y in range(1, len(self.tile)-1):
			nTile.append(self.tile[y][1:-1]);
		return nTile;

	def returnString(self):
		allRows = [];
		for y in self.tile:
			allRows.append("".join(y));
		return "\n".join(allRows);



class tileComp:
	def __init__(self, tile, key):
		fOptions = [tile, tile[::-1], [row[::-1] for row in tile], [row[::-1] for row in tile[::-1]]];
		# Generate borders
		self.options = [];
		for option in fOptions:
			self.options.append(option);
			option = list(zip(*reversed(option)));
			self.options.append(option);
			option = list(zip(*reversed(option)));
			self.options.append(option);
			option = list(zip(*reversed(option)));
			self.options.append(option);
		self.basicTiles = [];
		for option in self.options:
			self.basicTiles.append(tileBasic(option, genBordersNoFlips(option), key));
		self.key = key;


def genBordersNoFlips(tile):
	borders = {};
	borders[0] = list(tile[0]);

	# borders[2] = list(tile[-1][::-1]);
	borders[2] = list(tile[-1]);

	borderL = [];
	borderR = [];
	for l in tile:
		borderL.append(l[0]);
		borderR.append(l[-1]);

	borders[1] = list(borderR);

	# borders[3] = list(borderL[::-1]);
	borders[3] = list(borderL);

	return borders;


# Main Method
# Load File
sampleText = """Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...""".split("\n")
with open("day20.txt") as f:
	fInput = [sampleText, f.readlines()];

# Main method
for text in fInput:
	# Uncomment for debugger
	# db = DebugFile();
	# db.line(); #Put this inside the main loop to add lines to the debug file

	answer = 1;
	# END OF PREDEFINED
	tiles = [];
	curTile = 0;
	tile = [];
	numTiles = 0;

	# Load file
	for line in text:
		line = line.strip();
		if line == "":
			tiles += tileComp(tile, curTile).basicTiles;
			numTiles += 1;
			tile = [];
		elif line.startswith("Tile"):
			curTile = int(line.split(" ")[1][:-1]);
		else:
			tile.append([p for p in line]);
	tiles += tileComp(tile, curTile).basicTiles;
	numTiles += 1;

	startingTile = tiles[32] # Random number;
	usedTiles = [tiles[32].key];

	# Go all the way left
	while True:
		succ = False;
		for tile in tiles:
			if tile.borders[1] == startingTile.borders[3] and tile.key not in usedTiles:
				startingTile = tile;
				usedTiles.append(tile.key);
				succ = True;
				break;
		if not succ:
			break;

	while True:
		succ = False;
		for tile in tiles:
			if tile.borders[2] == startingTile.borders[0] and tile.key not in usedTiles:
				startingTile = tile;
				usedTiles.append(tile.key);
				succ = True;
				break;
		if not succ:
			break;

	corner = startingTile.key;

	# Now we know the top left corner so we just have to go row by row mapping the image
	for startingTile in tiles:
		startColumn = startingTile;
		usedTiles = [startingTile.key];
		pic = [];
		while True:
			cSucc = False;
			row = [startColumn];
			while True:
				rSucc = False;
				for tile in tiles:
					if tile.borders[3] == startingTile.borders[1] and tile.key not in usedTiles:
						startingTile = tile;
						usedTiles.append(tile.key);
						row.append(tile);
						rSucc = True;
						break;
				if not rSucc:
					pic.append(row);
					break;

			for tile in tiles:
				if tile.borders[0] == startColumn.borders[2] and tile.key not in usedTiles:
					startColumn = tile;
					usedTiles.append(tile.key);
					cSucc = True;
					break;
			if not cSucc:
				break;
			startingTile = startColumn;

		goodLens = all([sqrt(numTiles) == len(pic[i]) for i in range(len(pic))]);
		if goodLens and len(pic) == sqrt(numTiles):
			break;

	compRows = [];
	for r in pic:
		for y in range(len(r[0].removeBorders())):
			row = "";
			for t in r:
				row += "".join(t.removeBorders()[y]);
			compRows.append([char for char in row]);

	fullPictures = [tile.returnString() for tile in tileComp(compRows, 0).basicTiles];
	for picture in fullPictures:
		nPic = picture.split("\n");
		answer = picture.count("#");
		print(answer);
		succ = False;
		for i in range(len(nPic)-2):
			head = re.search("..................#.", nPic[i]);
			if head:
				body = re.search("#....##....##....###", nPic[i+1]);
				if body:
					tail = re.search(".#..#..#..#..#..#...", nPic[i+2]);
					if tail:
						succ = True;
						answer -= 15;
		if succ:
			break;



	# BEGINNING OF PREDEFINED
	print(answer);

	# Uncomment for debugger
	# print("Saved at %s" % db.startingFile);
	# del db;

# Return answer
os.system('echo ' + str(answer).strip() + '| clip');