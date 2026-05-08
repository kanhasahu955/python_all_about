# When you create a new object of a class, Python automatically calls the __init__() method to initialize the object’s attributes.

# The double underscores at both sides of the __init__() method indicate that Python will use the method internally. In other words, you should not explicitly call this method.

class Person:
    def __init__(self,name ,age,village='girisola'):
        self.name = name
        self.age = age
        self.village = village
        print('Initializing a new person...')
# creating an instance of the class
person1 = Person("Alice", 30)
print(person1.name)  # Output: Alice
print(person1.age)   # Output: 30
print(person1.village)  # Output: Unknown

    
# Use the __init__() method to initialize the object’s attributes.
# The __init__() doesn’t create an object but is automatically called after the object is created.