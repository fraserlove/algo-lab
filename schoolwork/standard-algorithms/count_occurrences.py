# Count Occurrences -  Higher Standard Algorithm
array = ["A","B","D","A","F","C","B","B","D","A","E","C","A","B","F","A"]

occurrences = 0
search_value = input("Enter a grade from A-F: ")
for counter in range(0, len(array)):
    if array[counter] == search_value:
        occurrences = occurrences + 1
print(search_value, "occurrences: ", occurrences)

# Set number of occurrences initally to 0
# Ask user to enter a value to search for in the array
# For each number in the range of 0 to the length of array (can use len(array) or manually type in array length)
# Check if element at the index of counter equals the search value
# If true increment occurrences by 1
