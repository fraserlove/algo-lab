#Kata URL: https://www.codewars.com/kata/5679aa472b8f57fb8c000047

def find_even_index(integers):
    place = 0
    got_answer = False
    while place < len(integers):
        left_total, right_total, i, j = 0, 0, 0, 1
        while i < place:
            left_total += integers[i]
            i += 1
        while j + place < len(integers):
            right_total += integers[j + place]
            j += 1
        place += 1
        if left_total == right_total:
            return (place - 1)
            got_answer = True
    if got_answer == False:
        return -1
