import random

class Account():
    def __init__(self, name, balance, intrate):
        self._pin = [chr(random.randint(48,57)) for i in range(4)]
        self._account_no = [chr(random.randint(48,57)) for i in range(8)]
        self._name = name
        self._balance = balance
        self._intrate = intrate

    def __str__(self):
        str = '\nPIN: {}\nAccount No: {}\nAccount Holder: {}\nBalance: {}\nInterest Rate: {}\n'\
        .format(''.join(self._pin), ''.join(self._account_no), self._name, self._balance, self._intrate)
        return str

    def deposit(self, amount):
        self._balance += amount

    def withdraw(self, amount):
        self._balance -= amount

    def getBalance(self):
        return '{:.2f}'.format(self._balance)

    def setBalance(self, amount):
        self._balance = amount

    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name

    def pinReminder(self):
        print(''.join(self._pin))

    def genNewPin(self):
        new = [chr(random.randint(48,57)) for i in range(4)]
        while new == self._pin:
            new = [chr(random.randint(48,57)) for i in range(4)]
        self._pin = new

account = Account('Fraser Love',400,0.6)
account.deposit(100)
print('Your balance is £{}'.format(account.getBalance()))
print(account)
account.genNewPin()
account.pinReminder()
