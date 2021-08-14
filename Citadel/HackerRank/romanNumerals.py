# Print Roman number equivalent for numbers 1-1000
numerals = {1000: 'M', 900: 'CM', 500: 'D', 400: 'CD', 100: 'C', 90: 'XC', 50: 'L', 40: 'XL', 10: 'X', 9: 'IX', 5: 'V', 4: 'IV', 1: 'I'};


def convert_numerals(number):
	out = "";
	for v, c in numerals.items():
		if number >= v:
			repeat, number = divmod(number, v)
			out += c * repeat
	return out


for i in range(1, 1001):
	print(convert_numerals(i))