#Kata URL: https://www.codewars.com/kata/52bc74d4ac05d0945d00054e

def first_non_repeating_letter(string):
    lst_lower = list(string.lower())
    s_chars = False
    for i in range (len(lst_lower)):
        if lst_lower.count(lst_lower[i]) == 1:
            s_chars = True
            return ((list(string))[i])
    if s_chars == False:
        return("")
