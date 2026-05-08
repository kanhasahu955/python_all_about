class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __bool__(self):
        if self.age < 18 or self.age > 65:
            return False
        return True


person = Person('Jane', 16)
print(bool(person))  # False



class Payroll:
    def __init__(self, length):
        self.length = length

    def __len__(self):
        print('len was called...')
        return self.length



payroll = Payroll(0)
print(bool(payroll))  # False

payroll.length = 10
print(bool(payroll))  # True