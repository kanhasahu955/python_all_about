from pprint import pprint


class Person:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value.strip() == '':
            raise ValueError('name cannot be empty')
        self._name = value

    @name.deleter
    def name(self):
        del self._name

pprint(Person.__dict__)

person = Person('John')
pprint(person.__dict__)
del person.name
pprint(person.__dict__)
print(person.name)
