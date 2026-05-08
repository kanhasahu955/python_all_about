class Person:
    def send():
        print('sending message...')

# calling the method using the class name
Person.send()  # Output: sending message...
# creating an instance of the class
person1 = Person()
# calling the method using the instance
person1.send()  # Output: sending message...

print(type(Person.send))  # Output: <class 'function'> (send is a function defined in the class)
print(type(person1.send))  # Output: <class 'method'> (send is a method bound to the instance)

print(isinstance(Person.send, type(Person.send)))  # Output: True (Person.send is an instance of the function type  class   since it's a function defined in the class  and not bound to any instance   
print(isinstance(person1.send, type(person1.send)))  # Output: True (person1.send is an instance of the method type class since it's a method bound to the instance)

print(type(Person.send) is type(person1.send)) # Output: False (Person.send is a function while person1.send is a method, so they are of different types)