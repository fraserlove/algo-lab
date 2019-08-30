def get_input():
    names, scores, percentages, grades = ([] for i in range(4))
    for counter in range(10):
        names.append(input('\nEnter the name of pupil {}: '.format(counter+1)).capitalize())
        scores.append(int(input('Enter {}\'s score: '.format(names[-1]))))
        percentages.append(round((scores[-1]/150)*100))
        if percentages[-1] >= 85:
            grades.append('A')
        elif percentages[-1] >= 70:
            grades.append('B')
        elif percentages[-1] >= 60:
            grades.append('C')
        elif percentages[-1] >= 50:
            grades.append('D')
        elif percentages[-1] >= 40:
            grades.append('E')
        else:
            grades.append('F')
    return names, scores, percentages, grades

def _output(names, scores, percentages, grades):
    print('\n\n\n\tName\t\tScore\t\tPercentage\tGrade')
    for i in range(len(names)):
        print('\t{}\t\t{}\t\t{}%\t\t{}'.format(names[i], scores[i], percentages[i], grades[i]))

names, scores, percentages, grades = get_input()
_output(names, scores, percentages, grades)
