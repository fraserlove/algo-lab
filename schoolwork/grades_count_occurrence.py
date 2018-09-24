def get_input():
    for i in range(0,20):
        grades.append(input('Enter the grade of student {}: '.format(i+1)))
    return grades

def occurrences(grades, letters):
    _output = [0,0,0,0,0,0]
    for grade in grades:
        for letter in letters:
            if letter == grade:
                _output[letters.index(letter)] += 1
    return _output

def display(_output, letters):
    for i in range(0,len(_output)):
        print('{}\'s: {}'.format(letters[i], _output[i])) 

grades = []
letters = ['A','B','C','D','E','F']
display(occurrences(get_input(), letters),letters)
