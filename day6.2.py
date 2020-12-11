with open("day6.txt") as f:
	text = f.readlines();

totalNL = 0
for line in text:
	if line == "\n":
		totalNL += 1;
print(totalNL);

# Gen passports
allGroups = [];
curGroup = "";
for pp in text:
	if pp == "\n":
		allGroups.append(curGroup);
		curGroup = "";
	else:
		if len(curGroup) > 0:
			curGroup += (" " + pp.rstrip());
		else:
			curGroup = pp.rstrip();
	if text.index(pp) == len(text) - 1:
		allGroups.append(curGroup);

allGroupsQuestion = [];
for group in allGroups:
	ngroup = group.replace(" ", "");
	curGroupQuest = {char: True for char in ngroup};
	curGroupQuest = list(curGroupQuest.keys());
	allGroupsQuestion.append([quest for quest in curGroupQuest if all([quest in grp for grp in group.split(" ")])]);

questionTotal = 0;
for group in allGroupsQuestion:
	questionTotal += len(group);

print(questionTotal);