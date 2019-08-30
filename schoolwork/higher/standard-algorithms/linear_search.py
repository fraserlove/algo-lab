# Linear Search -  Higher Standard Algorithm
array = [59,67,37,13,94,12,75,84,24,71]

found = False
search_value = int(input("Enter a integer to search for: "))
for counter in range(0, len(array)):
    if array[counter] == search_value:
        print("Found", search_value, "at position", counter)
        found = True
if found == False:
    print("Error: Program could not find value!")

# Set found intitally to false
# Ask user to enter a value to search for in the array
# For each number in the range of 0 to the length of array (can use len(array) or manually type in array length)
# Check if element at the index of counter equals the search value
# If true set found to true and send array index to display
# If after all elements in the array found is still false send and error message to display
