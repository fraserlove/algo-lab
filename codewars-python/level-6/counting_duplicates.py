#Kata URL: https://www.codewars.com/kata/54bf1c2cd5b56cc47f0007a1

def duplicate_count(text):
    lst = list(text.lower())
    chars_seen = []
    chars_found = []
    for char in lst:
        if char in chars_seen and char not in chars_found:
            chars_found.append(char)
        else:
            chars_seen.append(char)
    return len(chars_found)
