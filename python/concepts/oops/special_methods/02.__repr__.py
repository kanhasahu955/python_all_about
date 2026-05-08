class Person:
    def __init__(self, first_name, last_name, age):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age

    def __repr__(self):
        return f'Person("{self.first_name}","{self.last_name}",{self.age})'
    
    def __str__(self):
        return f'Person({self.first_name},{self.last_name},{self.age})'
    
person = Person('John', 'Doe', 25)
print(person)  # Output: Person("John","Doe",25)
print(repr(person))  # Output: Person("John","Doe",25) (repr returns the same string representation as __repr__)



# The main difference between __str__ and __repr__ method is intended audiences.

# The __str__ method returns a string representation of an object that is human-readable while the __repr__ method returns a string representation of an object that is machine-readable.