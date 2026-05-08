class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greeting(self):
        return f'Hi, I am {self.name}. I am {self.age} year old.'
    
print(type(Person))
print(isinstance(Person, type))


class_body = """
def __init__(self, name, age):
    self.name = name
    self.age = age

def greeting(self):
    return f'Hi, I am {self.name}. I am {self.age} year old.'
"""

class_dict = {}

Person = type('Person', (object,), class_dict)