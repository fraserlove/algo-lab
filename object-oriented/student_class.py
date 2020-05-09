class Student:

    # Class Variables - always the same for each instance
    # Called by instance.var or Class.var
    school = 'PHS'
    total_students = 0

    # Initialise method or constructor
    # Used to set up the object
    def __init__(self, first, last, age, form, merits):
        self.first = first
        self.last = last
        self.age = age
        self.year = 'S{}'.format(age - 11)
        self.form = '{}{}'.format(age - 11, form)
        self.email = '{}.{}_{}@school.com'.format(first, last, self.form)
        self.merits = merits

        # Updates class variable every time a new object is made
        Student.total_students += 1

    def display(self):
        disp_name = 'Name: {} {}'.format(self.first, self.last)
        disp_age = 'Age: {}'.format(self.age)
        disp_year = 'Year: {}'.format(self.year)
        disp_form = 'Form Class: {}'.format(self.form)
        disp_email = 'Email: {}'.format(self.email)
        disp_merits = 'Merits: {}'.format(self.merits)
        return disp_name, disp_age, disp_year, disp_form, disp_email, disp_merits, self.school

    def add_merits(self):
        added_merits = int(input('\nHow many merits do you want to give {} {}: '.format((self.first).capitalize(), (self.last).capitalize())))
        self.merits += added_merits
        print('\nSuccessfully Completed\n')
        print('Merits Added: {}'.format(added_merits))
        print('Student: {} {}'.format((self.first).capitalize(), (self.last).capitalize()))
        print('Merits Before: {}'.format(self.merits - added_merits))
        print('Merits Now: {}'.format(self.merits))
        return ''

    def sub_merits(self):
        subtract_merits = int(input('\nHow many merits do you want to subtract from {} {}: '.format((self.first).capitalize(), (self.last).capitalize())))
        self.merits -= subtract_merits
        print('\nSuccessfully Completed\n')
        print('Merits Subtracted: {}'.format(subtract_merits))
        print('Student: {} {}'.format((self.first).capitalize(), (self.last).capitalize()))
        print('Merits Before: {}'.format(self.merits + subtract_merits))
        print('Merits Now: {}'.format(self.merits))
        return ''

print(Student.total_students)

student_1 = Student('user', 'one', 16, 'D2', 13)
student_2 = Student('user', 'two', 12, 'C3', 6)
student_3 = Student('user', 'three', 17, 'M1', 5)

print(Student.total_students)

year = [student_1, student_2, student_3]

def display_class():
    for student in year:
        print(student.display())

def total_merits():
    total = 0
    for student in year:
        total += student.merits
    print('Total Merits: {}'.format(total))

display_class()
total_merits()

# There are two ways to call a methods and attributes in a class
# One where we specify the instance of the class and the method or attribute in that instance
# instance.method()
print(student_1.display())
# Or where you specify the lass and the method or attribute in the class then pass in the instance as an argument
# Class.method(instance)
print(Student.display(student_1))
