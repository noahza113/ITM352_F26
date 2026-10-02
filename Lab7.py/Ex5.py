celebs = ("Talor Swift", "Beyonce", "Adele", "Rihanna", "Michael Jackson")
ages = (33, 39, 34, 35, 43)

celeb_list = []
for celeb in celebs:
    celeb_list.append(celeb)

age_list = [age for age in ages]

celebs_dict = {"celebs": celeb_list, "ages": age_list}
print (celebs_dict)