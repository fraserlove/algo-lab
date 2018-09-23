"""
Developed by Fraser Love from 16/03/18 to 22/03/18 on CPTN-RX
"""

import random, os
lc_list = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
uc_list = []
n_list = ["0","1","2","3","4","5","6","7","8","9"]
char_list = ["!","\"","$","%","^","*","(",")","-","_","+","=","[","]","{","}",";",":","@","'","#","~","<",",",".",">","/","?","¬"]
s_char_list = ["!","\"","$","%","^","*","(",")","-","_","+","=","[","]","{","}",";",":","@","#","~","<",">","/","?"]
password = []
newline = False
u_name_spacing = []
info_spacing = []
p_name_spacing = []
auth_spacing = []

for i in lc_list:
    uc_list.append(i.upper())
print("-------------------------------------")
print("     Password Generator Program")
print("     By Fraser Love On 17/03/18")
print("-------------------------------------")
print("\n\n")
print("*************************************")
print(" \n               SETUP")
print("\n*************************************")
print("\n\n      Password Generation Types")
print("-------------------------------------")
print("\n  _______________________________________________________________")
print(" |                                                               |")
print(" |      Numbers = 0                                              |")
print(" |      Lowercase Letters = 1                                    |")
print(" |      Uppercase Letters = 2                                    |")  
print(" |      All Letters = 3                                          |")
print(" |      Special Characters = 4                                   |")
print(" |      Numbers and Letters = 5                                  |")   
print(" |      Numbers and Special Characters = 6                       |")
print(" |      Letters and Special Characters = 7                       |")
print(" |      Full Protection - Numbers, Letters and Characters = 8    |")
print(" |      Reccomended - Numbers, Letters and Some Characters = 9   |")
print(" |_______________________________________________________________|")
pass_type = int(input("\n Type The Number Of The Type Of Password Generation You Would Like: "))
print("\n-------------------------------------")
print("\n")

print("       Password Length Options")
print("-------------------------------------")

print("\n******************************************************")
print("\nWeak Password: 5 Characters and under")
print("Crack Time: Nearly Instantly")
print("\n******************************************************")
print("\nMedium Password: Between 5 and 10 Characters")
print("Crack Time: Between 5 Seconds and A Year")
print("\n******************************************************")
print("\nStrong Password: Between 10 and 15 Characters")
print("Crack Time: Between 10 Years and A Billion Years")
print("\n******************************************************")
print("\nUltra Secure Password: 15 Characters and Over")
print("Crack Time: A 100 Billion Years And Over")
print("\n******************************************************")
pass_length = int(input("What Length Do You Want Your Password To Be: "))
while pass_length < 2 or pass_length > 30:
    print("Invalid Length: Must be between 2 and 20")
    pass_length = int(input("What Length Do You Want Your Password To Be: "))
print("\n-------------------------------------")
print("\n")


if pass_type == 9:
    pt_output = "Numbers, Letters and Some Special Characters"
    for j in range(0, pass_length):
        rand_choice = random.randint(1,4)
        if rand_choice == 1:
            password.append(random.choice(lc_list))
        elif rand_choice == 2:
            password.append(random.choice(uc_list))
        elif rand_choice == 3:
          password.append(random.choice(n_list))
        elif rand_choice == 4:
          password.append(random.choice(s_char_list))

elif pass_type == 8:
    pt_output = "Numbers, Letters and All Characters"
    for j in range(0, pass_length):
        rand_choice = random.randint(1,4)
        if rand_choice == 1:
            password.append(random.choice(lc_list))
        elif rand_choice == 2:
            password.append(random.choice(uc_list))
        elif rand_choice == 3:
          password.append(random.choice(n_list))
        elif rand_choice == 4:
         password.append(random.choice(char_list))

elif pass_type == 7:
    pt_output = "Letters and Special Characters"
    for j in range(0, pass_length):
        rand_choice = random.randint(1,3)
        if rand_choice == 1:
            password.append(random.choice(lc_list))
        elif rand_choice == 2:
            password.append(random.choice(uc_list))
        elif rand_choice == 3:
            password.append(random.choice(char_list))

elif pass_type == 6:
        pt_output = "Numbers and Special Characters"
        for j in range(0, pass_length):
            rand_choice = random.randint(1,2)
            if rand_choice == 1:
                password.append(random.choice(n_list))
            elif rand_choice == 2:
                password.append(random.choice(char_list))

elif pass_type == 5:
    pt_output = "Numbers and Letters"
    for j in range(0, pass_length):
        rand_choice = random.randint(1,3)
        if rand_choice == 1:
            password.append(random.choice(lc_list))
        elif rand_choice == 2:
            password.append(random.choice(uc_list))
        elif rand_choice == 3:
          password.append(random.choice(n_list))

elif pass_type == 4:
    pt_output = "Special Characters"
    for j in range(0, pass_length):
         password.append(random.choice(char_list))

elif pass_type == 3:
    pt_output = "All Letters"
    for j in range(0, pass_length):
        rand_choice = random.randint(1,2)
        if rand_choice == 1:
            password.append(random.choice(lc_list))
        elif rand_choice == 2:
            password.append(random.choice(uc_list))

elif pass_type == 2:
    pt_output = "Uppercase Letters"
    for j in range(0, pass_length):
        password.append(random.choice(uc_list))

elif pass_type == 1:
    pt_output = "Lowercase Letters"
    for j in range(0, pass_length):
        password.append(random.choice(lc_list))

elif pass_type == 0:
    pt_output = "Numbers"
    for j in range(0, pass_length):
        password.append(random.choice(n_list))


print_pass = "".join(password)
print("\nPassword Generation Finished")
print("\nYour Specifications Were:")
print("Password Type: "+ pt_output)
print("Password Length: " + str(pass_length) + " characters")
print("\nYour Password: "+ "".join(password))
store = input("\nWould you to store the password in a text file along with a username - Type Y for yes or N for no: ")
if store == "Y" or store == "y":
    if os.path.isfile("Passwords/passwords.txt") == False:
        topnav = "Account Info             Username                      Password                 2FA Enabled         2FA Type"
        line = "\n-------------------------------------------------------------------------------------------------------------------"
        newline = True
    else:
        topnav = ""
        line = ""


    info_len = 25
    u_name_len = 30
    p_length = 25
    auth_len = 20
    info = input("What information would you like to give with the password (max 30 char): ")
    while len(info) > 30:
        print("Invalid Length: Try again")
        info = input("What information would you like to give with the password (max 30 char): ")
    u_name = input("What is your username (max 30 char): ")
    while len(u_name) > 30:
        print("Invalid Length: Try again")
        u_name = input("What is your username (max 30 char): ")
    auth = str(input("Do you have 2FA enabled on the account - Type Y for yes or N for no: "))
    if auth == "Y" or auth == "y":
        auth = "Yes"
        authtype = str(input("What type of 2FA was it - Type P for Phone or G for G-Authenticate: "))
        if authtype == "P" or authtype == "p":
            authtype = "Phone"
        elif authtype == "G" or authtype == "g":
            authtype = "G-Authenticate"
    else:
        auth = "No"
        authtype = ""
    auth_distance = auth_len - len(auth)
    p_distance = p_length - pass_length
    info_distance = info_len - len(info)
    u_name_distance = u_name_len - len(u_name)
    for i in range(0,info_distance):
        info_spacing.append(" ")
    for i in range(0,u_name_distance):
        u_name_spacing.append(" ")
    for i in range(0,p_distance):
        p_name_spacing.append(" ")
    for i in range(0,auth_distance):
        auth_spacing.append(" ")
    print("\nSuccessfull!")
    print("\nStored As:")
    print("\n " + info + "".join(info_spacing) + u_name + "".join(u_name_spacing) + "".join(password) + "".join(p_name_spacing) + auth + "".join(auth_spacing) + authtype)
    if not os.path.exists("Passwords"):
        os.makedirs("Passwords")
    file = open("Passwords/passwords.txt", "a")
    file_read = open("Passwords/passwords.txt", "r")
    file.write(topnav)
    file.write(line)
    file.write("\n" + info + "".join(info_spacing) + u_name + "".join(u_name_spacing) + "".join(password) + "".join(p_name_spacing) + auth + "".join(auth_spacing) + authtype)
    file.close()
