# define a class
class Person:
    pass

# create instance of the class
person1 = Person()

print(person1)  # Output: <__main__.Person object at 0x7f8b8c2e5d30>
print(type(person1))  # Output: <class '__main__.Person'>
print(isinstance(person1, Person))  # Output: True
print(isinstance(person1, object))  # Output: True
print(id(person1))  # Output: Memory address of the object (varies each time you run the program
print(dir(person1))  # Output: List of attributes and methods of the object
print(person1.__class__)  # Output: <class '__main__.Person'>
print(person1.__dict__)  # Output: {} (empty dictionary since no attributes have been
print(person1.__doc__)  # Output: None (no docstring defined for the class)
print(person1.__module__)  # Output: __main__ (the module where the class is defined)
print(person1.__weakref__)  # Output: None (no weak references to the object)
print(hex(id(person1)))  # Output: Memory address of the object in hexadecimal format (varies each time you run the program

print(type(Person))  # Output: <class 'type'> (Person is a class, which is an instance of the type class)
print(Person.__name__)  # Output: Person (the name of the class)
print(Person.__bases__)  # Output: (<class 'object'>,)
print(Person.__dict__)  # Output: Dictionary containing the class's attributes and methods
print(Person.__doc__)  # Output: None (no docstring defined for the class)
print(Person.__module__)  # Output: __main__ (the module where the class is defined)
print(Person.__weakref__)  # Output: None (no weak references to the class