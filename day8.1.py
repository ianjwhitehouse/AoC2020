import nltk;


with open("day8.txt") as f:
	text = f.readlines();

text[32] = "nop " + text[32].split(" ")[1];
visited = [];
accumulator = 0;
curLine = 0;
while curLine < len(text):
	line = text[curLine][:-1];
	if visited.count(curLine) > 200:
		print("Oh No");
		print(list(nltk.FreqDist(visited).keys())[:10])
		break;
	visited.append(curLine);
	if line.split(" ")[0] == "acc":
		if line.split(" ")[1].startswith("+"):
			accumulator += int(line.split(" ")[1][1:]);
		else:
			accumulator -= int(line.split(" ")[1][1:]);
		curLine += 1;

	elif line.split(" ")[0] == "jmp":
		if line.split(" ")[1].startswith("+"):
			curLine += int(line.split(" ")[1][1:]);
		else:
			curLine -= int(line.split(" ")[1][1:]);

	else:
		curLine += 1;

print(accumulator);

with open("day8Debug.txt", "w+") as file:
	file.writelines([str(line) + ": " + text[line] for line in visited]);