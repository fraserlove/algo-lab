# Finding Maximum -  Higher Standard Algorithm
array = [59,67,37,13,94,12,75,84,24,71]

maximum = array[0]
for counter in range(0, len(array)):
    if array[counter] > maximum:
        maximum = array[counter]
print("Maximum Value: ", maximum)

# Set maximum value initally to first element in array
# For each number in the range of 0 to the length of array (can use len(array) or manually type in array length)
# Check if element at the index of counter is more than current maximum
# If true set maximum to that element in the array
