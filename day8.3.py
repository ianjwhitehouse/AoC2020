with open("day8Debug.txt") as f:
	text = f.readlines();

nText = []
for i in range(1, len(text)):
	nText.append([text[i-1], text[i]]);

searchList = [nText.count(val) for val in nText];
print(nText[searchList.index(max(searchList))]);