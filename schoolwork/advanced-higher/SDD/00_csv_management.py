import csv

class User():
    def __init__(self, args):
        self.email = args[0]
        self.f_name = args[1]
        self.s_name = args[2]
        self.percentage = args[3]

    def getDetails(self):
        return self.email, self.f_name, self.s_name, self.percentage

users = []
unique = []

def find_min(users):
    min = users[0].percentage
    for user in users:
        if user.percentage < min:
            min = user.percentage
    return min

def find_max(users):
    max = users[0].percentage
    for user in users:
        if user.percentage > max:
            max = user.percentage
    return max

def csv_management():
    with open('data/input/input_data.csv', 'r') as file:
        for row in csv.reader(file, delimiter=','):
            users.append(User(row))
        with open('data/output/output_data.csv', 'w') as file:
            writer = csv.writer(file, delimiter=',')
            for user in users:
                if user.email not in unique:
                    writer.writerow(user.getDetails())
                    unique.append(user.email)

def main():
    csv_management()
    print("\n{} records in original file".format(len(users)))
    print("New file created with {} records".format(len(unique)))
    print("{} duplicates removed".format(len(users) - len(unique)))
    print("Minimum Prelim Percentage: {:.0f}%".format(float(find_min(users))*100))
    print("Maximum Prelim Percentage: {:.0f}%\n".format(float(find_max(users))*100))

main()
