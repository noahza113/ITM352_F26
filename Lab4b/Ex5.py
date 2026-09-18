#Ask the user for a sentence (using input())
#Turn the sentence into a list of stings (using split())
#Reverse the list
#Join the list back into a string (using join())
#Name: Noah Zane
#Date: Sept 18, 2026

sentence = input("Enter a sentence: ")
words = sentence.split()
words.reverse()
reversed_sentence = " ".join(words)
print("Reversed sentence:", reversed_sentence)

joined_sentence = sentence + " " + reversed_sentence
print("Joined sentence:", joined_sentence)