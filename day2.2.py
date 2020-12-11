total = 0;
with open("day2.txt") as f:
	text = f.readlines();
	for t in text:
		t = t.split(" ");
		mini = int(t[0].split("-")[0]);
		maxi = int(t[0].split("-")[1]);
		char = t[1][0];
		if (t[2][mini - 1] == char) != (t[2][maxi - 1] == char):
			total += 1;

print(total);