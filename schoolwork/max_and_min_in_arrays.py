def _input():
    for i in range(5):
        name_list.append(str(input('Please enter pupil %s\'s name: '%str(i+1))))
        score_list.append(int(input('What did %s score: '%name_list[-1])))
    output()

def _max(array, n_array):
    maximum = array[0]
    name = n_array[0]
    for number in array:
        if number > maximum:
            maximum = number
            name = n_array[array.index(number)]
    return maximum, name

def _min(array, n_array):
    minimum = array[0]
    name = n_array[0]
    for number in array:
        if number < minimum:
            minimum = number
            name = n_array[array.index(number)]
    return minimum, name


def output():
    print('--------------------OUTPUT------------------')
    print('')
    print('--------------MAXIMUM------------')
    print('Name: ' + str(_max(score_list, name_list)[1]))
    print('Score: ' + str(_max(score_list, name_list)[0]))
    print('--------------MAXIMUM------------')
    print('')
    print('--------------MINIMUM------------')
    print('Name: ' + str(_min(score_list, name_list)[1]))
    print('Score: ' + str(_min(score_list, name_list)[0]))
    print('--------------MINIMUM------------')
    print('')
    print('--------------------OUTPUT------------------')


name_list = []
score_list = []
_input()
