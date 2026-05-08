# class Person:
#     def __init__(self, first_name, last_name, age):
#         self.first_name = first_name
#         self.last_name = last_name
#         self.age = age

# john = Person('John', 'Doe', 25)
# jane = Person('Jane', 'Doe', 25)

# print(john == jane)  # Output: False (john and jane are different objects in memory)
# print(john is jane)  # Output: False (john and jane are different objects in memory)


# class Person:
#     def __init__(self, first_name, last_name, age):
#         self.first_name = first_name
#         self.last_name = last_name
#         self.age = age

#     def __eq__(self, other):
#         return self.age == other.age
    
# john = Person('John', 'Doe', 25)
# jane = Person('Jane', 'Doe', 25)
# print(john == jane)  # True    



# class Person:
#     def __init__(self, first_name, last_name, age):
#         self.first_name = first_name
#         self.last_name = last_name
#         self.age = age

#     def __eq__(self, other):
#         return self.age == other.age

# john = Person('John', 'Doe', 25)
# mary = Person('Mary', 'Doe', 27)
# print(john == mary)  # False
# john = Person('John', 'Doe', 25)
# print(john == 20) #AttributeError: 'int' object has no attribute 'age'


class Person:
    def __init__(self, first_name, last_name, age):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age

    def __eq__(self, other):
        if isinstance(other, Person):
            return self.age == other.age

        return False


john = Person('John', 'Doe', 25)
jane = Person('Jane', 'Doe', 25)
mary = Person('Mary', 'Doe', 27)

print(john == jane)  # True
print(john == mary)  # False


john = Person('John', 'Doe', 25)
print(john == 20)  # False