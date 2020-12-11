with open("day8.txt") as f:
	text = f.readlines();

goal = 0;
all = [];
for line in text:
	if line.split(" ")[0] == "nop" or line.split(" ")[0] == "jmp":
		if line.split(" ")[1].startswith("+"):
			if text.index(line) + int(line.split(" ")[1][1:]) == goal:
				all.append(text.index(line));
				break;
		else:
			if text.index(line) - int(line.split(" ")[1][1:]) == goal:
				all.append(text.index(line));
				break;
print(all);