name_list = list(input("What is your name: "))
for char in name_list:
    name_list[name_list.index(char)] = ord(char)
    print('{} : {}'.format(char, name_list[name_list.index(int(ord(char)))]))
