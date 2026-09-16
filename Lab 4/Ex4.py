#Try to append to a tuple. It won't work
#Name: Noah Zane
#Date: Sept 16, 2026

survey_respondents = (1012, 1035, 1021, 1053)
survey_respondents.append(1067) #This will raise an AttributeError because tuples are immutable

survey_respondents = survey_respondents + (1054,)
print("Updated Survey Respondents:", survey_respondents)