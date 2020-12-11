class bag:
	def __init__(self, name, rules):
		self.name = name;
		# rules = [[number, name]]
		self.rules = rules;

	def shiny(self, bags):
		if any([r[1] == "shiny gold" for r in self.rules]):
			return True;
		else:
			for r in self.rules:
				name = r[1];
				for bag in bags:
					if bag.name == name:
						if bag.shiny(bags):
							return True;
		return False;

	def get_num_of_bags(self, bags):
		total = 0;
		for r in self.rules:
			name = r[1];
			amount = r[0]
			for bag in bags:
				if bag.name == name:
					total += (amount * bag.get_num_of_bags(bags));
		if total != 0:
			return total + 1;
		return 1;

with open("day7.txt") as f:
	text = f.readlines();

bags = [];
for rule in text:
	name = rule.split(" bags contain ")[0];
	rules = [];
	rule = rule.split(" bags contain ")[1].replace(".\n", "");
	for r in rule.split(", "):
		if r != "no other bags":
			nR = r.split(" ");
			rules.append([int(nR[0]), " ".join(nR[1:3])]);
	bags.append(bag(name, rules));

for bag in bags:
	print(bag.name, bag.shiny(bags));

print([bag.shiny(bags) for bag in bags].count(True));

for bag in bags:
	if bag.name == "shiny gold":
		print(bag.get_num_of_bags(bags) - 1);