import random

class Account():
    def __init__(self, balance, intrate):
        self._account_no = [chr(random.randint(48,57)) for i in range(8)]
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

class soleAccount(Account):
    def __init__(self, name, balance, intrate):
        Account.__init__(self, balance, intrate)
        self._pin = [chr(random.randint(48,57)) for i in range(4)]
        self._name = name

    def genNewPin(self):
        new = [chr(random.randint(48,57)) for i in range(4)]
        while new == self._pin:
            new = [chr(random.randint(48,57)) for i in range(4)]
        self._pin = new
        return self._pin

    def pinReminder(self):
        return ''.join(self._pin)

    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name

class jointAccount(Account):
    def __init__(self, names, balance, intrate):
        Account.__init__(self, balance, intrate)
        self._pin = [chr(random.randint(48,57)) for i in range(4)] * 2
        self._name = names

    def genNewPin(self):
        new = [chr(random.randint(48,57)) for i in range(4)]
        while new == self._pin:
            new = [chr(random.randint(48,57)) for i in range(4)]
        self._pin = new
        return self._pin

    def pinReminder(self):
        return ''.join(self._pin)

    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name

class savingsAccount(soleAccount):
    def __init__(self, names, balance, intrate):
        soleAccount.__init__(self, name, balance, intrate)
        self._withdrawls = []

    def withdraw(self, amount):
        self._balance -= amount
        self._withdrawls.append(amount)

class goldAccount(soleAccount):
    def __init__(self, names, balance, intrate):
        soleAccount.__init__(self, name, balance, intrate)
        self._overdraft = 0

    def setOverdraft(self, amount):
        self._overdraft += amount

    def getOverdraft(self):
        return self._overdraft

    def withdraw(self, amount):
        self._balance -= amount
