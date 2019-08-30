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
duplicates = []

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

def create_record_array():
    with open("data/data.csv", newline='') as file:
        for row in csv.reader(file, delimiter=','):
            users.append(User(row))

def write_to_file():
    with open("data/output_data.csv", "w", newline='') as file:
        writer = csv.writer(file, delimiter=',')
        for user in users:
            if user.email not in duplicates:
                writer.writerow(user.getDetails())
                duplicates.append(user.email)

def main():
    create_record_array()
    print("\n{} records in original file".format(len(users)))
    write_to_file()
    print("New file created with {} records".format(len(duplicates)))
    print("{} duplicates removed".format(len(users) - len(duplicates)))
    print("Minimum Prelim Percentage: {:.0f}%".format(float(find_min(users))*100))
    print("Maximum Prelim Percentage: {:.0f}%\n".format(float(find_max(users))*100))

main()
