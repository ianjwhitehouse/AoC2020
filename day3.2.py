# Function
def checkTrees(map, xCoord, yCoord, xChange, yChange):
	total = 0;
	while yCoord < len(map):
		# print(yCoord);
		if map[yCoord][xCoord] == "#":
			# print("Tree")
			total += 1;

		yCoord += yChange;
		xCoord += xChange;

	return total

# Create Map
map = [];
with open("day3.txt") as f:
	text = f.readlines();
	thisX = [];
	for t in text:
		map.append(750 * [i for i in t[:-1]]);

print("Map Loaded %d" %len(map));
total = 1;

for i in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
	total *= checkTrees(map, 0, 0, i[0], i[1]);

print(total);