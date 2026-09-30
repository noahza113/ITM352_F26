test_cases = [
	[1, "hello", 3.14],
	[42, "hello", 3.14, True, None, "Python", 7],
	[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
]

for values in test_cases:
	if len(values) < 5:
		print("The list contains fewer than 5 elements.")
	elif len(values) <= 10:
		print("The list contains between 5 and 10 elements.")
	else:
		print("The list contains more than 10 elements.")