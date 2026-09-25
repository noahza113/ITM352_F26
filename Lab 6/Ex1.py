emotions = ("suprise", "sad", "fear", "happy")

is_it_true = emotions[3] == "happy" and len(emotions) > 3
print(is_it_true)
# print(emotions[3] == "happy" and len(emotions) > 3)

if emotions[3] == "happy":
    print("True")
else:
    print("False")