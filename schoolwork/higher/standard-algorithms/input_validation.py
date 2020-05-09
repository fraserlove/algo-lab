# Input Validation -  Higher Standard Algorithm

user_input = int(input("Enter an integer between 0 - 10:"))
while user_input < 0 or user_input > 10:
    print("Input Error! The integer you entered was not valid, try again: ")
    user_input = int(input("Enter an integer between 0 - 10:"))

# Must have an inital user input
# Then a while loop to check the inital entry and if true
# Send and error message to screen
# Ask for user input again
# Until a correct input is given (while loop validated false)
