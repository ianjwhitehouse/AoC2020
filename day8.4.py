import nltk;


with open("day8.txt") as f:
	text = f.readlines();

pChanges = [text.index(line) for line in text if line.startswith("nop") or line.startswith("jmp")];
originalText = text[:];


for change in pChanges:
	print("Change %s/%s" %(pChanges.index(change), len(pChanges)));
	text = originalText[:];
	success = True;

	if text[change].startswith("nop"):
		text[change] = "jmp " + text[change].split(" ")[1];
	elif text[change].startswith("jmp"):
		text[change] = "nop " + text[change].split(" ")[1];

	visited = [];
	accumulator = 0;
	curLine = 0;
	while curLine < len(text):
		line = text[curLine][:-1];
		if visited.count(curLine) > 50:
			#print("Oh No");
			#print(list(nltk.FreqDist(visited).keys())[:10]);
			success = False;
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
	if success:
		print(accumulator);