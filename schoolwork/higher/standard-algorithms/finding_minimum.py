# Finding Minimum -  Higher Standard Algorithm
array = [59,67,37,13,94,12,75,84,24,71]

minimum = array[0]
for counter in range(0, len(array)):
    if array[counter] < minimum:
        minimum = array[counter]
print("Minimum Value: ", minimum)

# Set minimum value initally to first element in array
# For each number in the range of 0 to the length of array (can use len(array) or manually type in array length)
# Check if element at the index of counter is less than current minimum
# If true set minimum to that element in the array
