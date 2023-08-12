'''
Basic functions required for data handling/processing.
'''

def string_to_2d_int_array(string, end):
    ''' Converts a string to a 2D-Array of integers and slices off a certain amount end in each sub-array. '''
    temp = []
    result = []
    # Removing common list or tuple presentation
    for word in string.split(','):
        word = word.replace('[', '')
        word = word.replace(']', '')
        word = word.replace('(', '')
        word = word.replace(')', '')
        if word != '':
            temp.append(int(word))
    for i in range(0,len(temp),end):
        result.append((temp[i:i+end]))
    return result

def string_to_2d_float_array(string, end):
    ''' Converts a string to a 2D-array of real numbers and slices off a certain amount, end, in each sub-array. '''
    temp, result = [], []
    # Removing common list or tuple presentation
    for word in string.split(','):
        word = word.replace('[', '')
        word = word.replace(']', '')
        word = word.replace('(', '')
        word = word.replace(')', '')
        temp.append(float(word))
    for i in range(0,len(temp),end):
        result.append((temp[i:i+end]))
    return result

def v_strip_2d_array(array, column):
    ''' Removes all elements after a specific column in a 2D-array. '''
    result = []
    for y in range(len(array)):
        result.append(array[y][:column])
    return result  

def string_to_int_array(string):
    ''' Converts a string to an array of integers. '''
    result = []
    # Removing common list or tuple presentation
    for word in string.split(','):
        word = word.replace('(', '')
        word = word.replace(')', '')
        word = word.replace('[', '')
        word = word.replace(']', '')
        result.append(int(word))
    return result

def string_to_float_array(string):
    ''' Converts a string to an array of real numbers. '''
    result = []
    # Removing common list or tuple presentation
    for word in string.split(','):
        word = word.replace('(', '')
        word = word.replace(')', '')
        word = word.replace('[', '')
        word = word.replace(']', '')
        result.append(float(word))
    return result

def div_non_zero(numerator, denominator):
    ''' A special divsion function to avoid execution errors associated with dividing by 0. '''
    if denominator != 0:
        return numerator / denominator
    else:
        return 0

def map(value, left_min, left_max, right_min, right_max):
    ''' A function to map a value from one range of values to another. Provides boundary exceptions so that mapping is always within output range. '''
    left = float(left_max) - float(left_min)
    right = right_max - right_min
    # Convert left range into a 0-1 range
    value_scaled = div_non_zero(float(value - left_min), float(left))
    # Convert 0-1 range into right range
    mapped_value =  right_min + (value_scaled * right)
    if mapped_value > right_max:
        mapped_value = right_max
    elif mapped_value < right_min:
        mapped_value = right_min
    return mapped_value

def convert_to_int_array(array):
    ''' Converts an array of real numbers or strings to an array of integers. '''
    result = []
    for element in array:
        result.append(int(element))
    return result

def convert_to_int_2d_array(array):
    ''' Converts a 2D-array of real numbers or strings to an array of integers. '''
    result = []
    for row in array:
        new_row = []
        for element in row:
            new_row.append(int(element))
        result.append(new_row)
    return result