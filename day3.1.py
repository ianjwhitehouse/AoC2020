# Function
def checkAround(map, x, y):
	for row in map[y-1:y+2]:
		for coord in row[x-1:x+2]:
			if coord == "#":
				return True;
	return False;

# Create Map
map = [];
with open("day3.txt") as f:
	text = f.readlines();
	thisX = [];
	for t in text:
		map.append(750 * [i for i in t[:-1]]);

print("Map Loaded %d" %len(map));
yCoord = 0;
xCoord = 0;
total = 0;

while yCoord < len(map):
	#print(yCoord);
	if map[yCoord][xCoord] == "#":
		print("Tree")
		total += 1;

	yCoord += 1;
	xCoord += 3;

print(total);