#Get a URL from the user, clean it, and then extract the domain name and TLD
#Name: Noah Zane
#Date: Sept 18, 2026

url = input("Enter a URL: ")

cleaned_url = url.replace("https://", "")
cleaned_url = cleaned_url.replace("/", "")
print("Cleaned URL:", cleaned_url)

parts = cleaned_url.split(".")
print("The parts are:", parts)

domain_name = parts[1]
tld = parts[2]
print("The domain name is:", domain_name)
print("The TLD is:", tld)