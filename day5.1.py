# Functions
def get_row(string):
	lowBound = 0;
	highBound = 127;
	for chr in string:
		half = round((highBound - lowBound)/2, 0);
		if (highBound - lowBound) == 1:
			if chr == "F":
				return lowBound;
			else:
				return highBound;
		else:
			if chr == "F":
				highBound -= half;
			else:
				lowBound += half;

def get_col(string):
	lowBound = 0;
	highBound = 7;
	for chr in string:
		half = round((highBound - lowBound)/2, 0);
		if (highBound - lowBound) == 1:
			if chr == "L":
				return lowBound;
			else:
				return highBound;
		else:
			if chr == "L":
				highBound -= half;
			else:
				lowBound += half;


# Main Method
with open("day5.txt") as f:
	text = f.readlines();

allIds = [];
for bp in text:
	allIds.append((get_row(bp[:7]) * 8) + get_col(bp[7:]));

print(max(allIds))
done = False;
for row in range(0, 127):
	if done:
		break;
	for column in range(0, 7):
		thisID = ((row * 8) + column);
		if not thisID in allIds:
			if thisID + 1 in allIds:
				if thisID - 1 in allIds:
					done = True;
					break;
print(thisID);