class Person:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hi, it's {self.name}"
    
# class Employee:
#     def __init__(self, name, job_title):
#         self.name = name
#         self.job_title = job_title

#     def greet(self):
#         return f"Hi, it's {self.name}"
    
class Employee(Person):
    def __init__(self, name, job_title):
        self.name = name
        self.job_title = job_title

employee = Employee('John', 'Python Developer')
print(employee.greet())

person = Person('Jane')
print(type(person))

employee = Employee('John', 'Python Developer')
print(type(employee))

person = Person('Jane')
print(isinstance(person, Person))  # True

employee = Employee('John', 'Python Developer')
print(isinstance(employee, Person))  # True
print(isinstance(employee, Employee))  # True
print(isinstance(person, Employee))  # False

print(issubclass(Employee, Person)) # True