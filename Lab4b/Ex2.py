#Properly format an inputed name in title case

raw_name = input("Enter your name: ")

stripped_name = raw_name.strip(" rka")
print("Stripped name:", stripped_name)

title_case_name = stripped_name.title()
print("Your name in title case is:", title_case_name)