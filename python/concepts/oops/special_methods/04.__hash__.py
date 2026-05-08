# class Person:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
        
# p1 = Person('John', 22)
# p2 = Person('Jane', 22)        

# print(hash(p1))
# print(hash(p2))


# class Person:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age

#     def __eq__(self, other):
#         return isinstance(other, Person) and self.age == other.age

# print(hash(Person('John', 22))) # unhashable type: 'Person'

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __eq__(self, other):
        return isinstance(other, Person) and self.age == other.age

    def __hash__(self):
        return hash(self.age)
    
p1 = Person('John', 22)
p2 = Person('Jane', 22)
print(hash(p1))  # Output: hash value based on the age of p1
print(hash(p2))  # Output: hash value based on the age of p2 (