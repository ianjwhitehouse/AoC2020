# Function
def validate(key, val):
	if key == "byr":
		if val.isnumeric() and len(val) == 4:
			if 1920 <= int(val) <= 2002:
				return True;
	elif key == "iyr":
		if val.isnumeric() and len(val) == 4:
			if 2010 <= int(val) <= 2020:
				return True;
	elif key == "eyr":
		if val.isnumeric() and len(val) == 4:
			if 2020 <= int(val) <= 2030:
				return True;
	elif key == "hgt":
		if val.endswith("cm"):
			if 150 <= int(val[:-2]) <= 193:
				return True;
		elif val.endswith("in"):
			if 59 <= int(val[:-2]) <= 76:
				return True;
	elif key == "hcl":
		if val[0] == "#" and len(val) == 7:
			try:
				int(val[1:], 16);
				return True;
			except:
				return False;
	elif key == "ecl":
		colors = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"];
		return val in colors;
	elif key == "pid":
		if val.isnumeric() and len(val) == 9:
			return True;
	elif key == "cid":
		return True;
	return False;


# Open File
with open("day4.txt") as f:
	text = f.readlines();

totalNL = 0
for line in text:
	if line == "\n":
		totalNL += 1;
print(totalNL);

# Gen passports
allPassport = [];
curPassport = "";
for pp in text:
	if pp[:-1] == "":
		allPassport.append(curPassport);
		curPassport = "";
	else:
		if len(curPassport) > 0:
			curPassport += (" " + pp.rstrip());
		else:
			curPassport = pp.rstrip();
	if text.index(pp) == len(text) - 1:
		allPassport.append(curPassport);

nAllPassports = [];
for pp in allPassport:
	curPassport = {}
	pp = pp.split(" ");
	for p in pp:
		if p.split(":")[0] in ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"]:
			curPassport[p.split(":")[0]] = p.split(":")[1];
	nAllPassports.append(curPassport);

totalSuccess = 0;
for pp in nAllPassports:
	if all([validate(key, value) for key, value in pp.items()]) and len(pp.keys()) >= 7:
		if len(pp.keys()) == 8:
			totalSuccess += 1;
		elif not "cid" in pp.keys():
			totalSuccess += 1;

print(totalSuccess);
pass;