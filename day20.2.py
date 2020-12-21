# Common Inputs
import string;
import os;
from numpy import prod;
from copy import deepcopy;
from math import cos, sin, degrees, radians, gcd, sqrt;
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
def genBorders(tile):
	borders = {};
	borders[0, 0] = tile[0];
	borders[0, 1] = tile[0][::-1];

	borders[2, 0] = tile[-1][::-1];
	borders[2, 1] = tile[-1];

	borderL = [];
	borderR = [];
	for l in tile:
		borderL.append(l[0]);
		borderR.append(l[-1]);

	borders[1, 0] = borderR[::-1];
	borders[1, 1] = borderR;

	borders[3, 0] = borderL;
	borders[3, 1] = borderL[::-1];

	return borders;


def genBordersNoFlips(tile):
	borders = {};
	borders[0, 0] = tile[0];

	borders[2, 0] = tile[-1][::-1];

	borderL = [];
	borderR = [];
	for l in tile:
		borderL.append(l[0]);
		borderR.append(l[-1]);

	borders[1, 0] = borderR[::-1];

	borders[3, 0] = borderL;

	return borders;



def manipulate(tile, rotation, yFlip, xFlip):
	try:
		xFlip = xFlip[0];
		nTile = [];
		for i in range(xFlip):
			for line in tile:
				nTile.append(line[::-1]);
			tile = nTile;
	except:
		pass;

	try:
		yFlip = yFlip[0];
		for y in range(yFlip):
			tile = tile[::-1];
	except:
		pass;

	try:
		rotation = rotation[0];
		for i in range(rotation):
			nTile = [];
			pixes = {};
			for y in range(len(tile)):
				for x in range(len(tile[0])):
					pixes[len(tile[0]) - (y + 1), x] = tile[y][x];

			for y in range(len(tile)):
				curLine = [];
				for x in range(len(tile[0])):
					curLine.append(pixes[x, y]);
				nTile.append(curLine);
			tile = nTile;
	except:
		pass;
	return tile;


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
	tiles = {};
	curTile = 0;
	tile = [];

	# Load file
	for line in text:
		line = line.strip();
		if line == "":
			borders = genBorders(tile);
			tiles[curTile] = [tile, borders, False];
			tile = [];
		elif line.startswith("Tile"):
			curTile = int(line.split(" ")[1][:-1]);
		else:
			tile.append([p for p in line]);
	borders = genBorders(tile);
	tiles[curTile] = [tile, borders, False];
	tile = [];

	# Manipulate image
	print(manipulate([[1, 2], [3, 4]], 1, 0, 0));

	nTiles = {key: tile for key, tile in tiles.items()};
	complete = False;
	# This works for flips but not rotates!!!!!
	while not complete:
		print("New Attempt")
		tiles = nTiles;
		nTiles = {};

		# list all borders
		allBorders = {};
		for key in tiles.keys():
			for bKey, items in tiles[key][1].items():
				allBorders[key, bKey[0], bKey[1]] = items;

		# Search for matching borders
		for key, tile in tiles.items():
			matchingBorders = [];
			Bs = tile[1];
			for bKey, border in Bs.items():
				for aBKey, aBorder in allBorders.items():
					if aBorder == border and key != aBKey[0]:
						matchingBorders.append([bKey, aBKey]);
			tile.append(matchingBorders);

		doneOne = False;
		for key, tile in tiles.items():
			if not tile[2] and not doneOne:
				sides = [[], [], [], []];
				rotations = [0];
				yFlips = [];
				xFlips = [];
				for border in tile[3]:
					sides[border[0][0]].append((border[1][0], border[1][1]));
					# rotations.append(border[1][1] - border[0][0]);
					if border[0][0] in [1, 3]:
						yFlips.append(abs(border[1][2] - border[0][1]));
					else:
						xFlips.append(abs(border[1][2] - border[0][1]));
					allLists = [val for val in sides + [rotations, yFlips, xFlips] if len(val) > 0];
				if all([lst.count(lst[0]) == len(lst) for lst in allLists]):
					nT = manipulate(tile[0], rotations, yFlips, xFlips);
					succ = True;
					doneOne = True;
				else:
					nT = tile[0];
					succ = False;
				nTiles[key] = [nT, genBorders(nT), succ];
			else:
				nTiles[key] = [tile[0], genBorders(tile[0]), tile[2]];
		complete = all([nTiles[key][2] for key in nTiles.keys()]);
	tiles = nTiles;

	# Find a middle
	nTiles = {}
	for key, tile in tiles.items():
		nTiles[key] = [tile[0], genBordersNoFlips(tile[0])];
	tiles = nTiles;

	allBorders = {};
	for key in tiles.keys():
		for bKey, items in tiles[key][1].items():
			allBorders[key, bKey[0], bKey[1]] = items;

	for key, tile in tiles.items():
		matchingBorders = [];
		Bs = tile[1];
		for bKey, border in Bs.items():
			for aBKey, aBorder in allBorders.items():
				if aBorder == border and key != aBKey[0]:
					matchingBorders.append([bKey, aBKey]);
		tile.append(matchingBorders);

	for key, tile in tiles.items():
		if len(tile[2]) == 2:
			sides = [x[0][0] for x in tile[2]];
			if sides.count(1) == 1 and sides.count(2) == 1:
				break;

	topLeft = key;
	rowStart = tiles[topLeft];
	rotation = 0;
	picture = [];
	rowRot = 0;
	for y in range(int(sqrt(len(tiles)))):
		curTile = rowStart;
		row = [(curTile[0], rotation)];
		for x in range(int(sqrt(len(tiles))) - 1):
			row.append((curTile[0], rotation))
			tBounds = {};
			for bound in curTile[2]:
				tBounds[(bound[0][0] + rotation) % 4] = (bound[1][0], bound[1][1]);
			nextT = tBounds[1];
			rotation = nextT[1] - 3;
			if rotation < 0:
				rotation = 4 - rotation;
			curTile = tiles[nextT[0]];
		print("row solved");
		picture.append(row);

		if y < int(sqrt(len(tiles))) - 1:
			tBounds = {};
			for bound in rowStart[2]:
				tBounds[(bound[0][0] + rowRot) % 4] = (bound[1][0], bound[1][1]);
			nextT = tBounds[2];
			rowRot = nextT[1];
			if rowRot < 0:
				rowRot = 4 - rowRot;
			rowStart = tiles[nextT[0]];
	print("Pic Loaded");

	nPic = [];
	for row in picture:
		nRow = [];
		for square in row:
			nRow.append(manipulate(square[0], [square[1]], [0], [0]));
		nPic.append(nRow);
	print("Rots Preformed");

	allRows = [];
	for row in nPic:
		nRow = [];
		for square in row:
			square = square[1:-1];
			square = [r[1:-1] for r in square];
			nRow.append(square);
		for y in range(len(square)):
			curRow = "";
			for square in nRow:
				curRow += "".join(square[y]);
			allRows.append(curRow);

	finalPicture = "\n".join(allRows);
	print(finalPicture);
	print("Completely loaded");





	# BEGINNING OF PREDEFINED
	print(answer);

	# Uncomment for debugger
	# print("Saved at %s" % db.startingFile);
	# del db;

# Return answer
os.system('echo ' + str(answer).strip() + '| clip');