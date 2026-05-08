# class Counter:
#     def __init__(self):
#         self.count  = 0
#     def increment(self):
#         self.count += 1
#     def decrement(self):
#         self.count -= 1
#     def get_count(self):
#         return self.count
    
# counter = Counter()
# counter.increment()
# counter.increment()
# print(counter.get_count())  # Output: 2
# counter.decrement()
# print(counter.get_count())  # Output: 1 

# counter.count = 100  # This directly modifies the count attribute, which can lead to unexpected behavior
# print(counter.get_count())  # Output: 100 (the get_count method now returns the



class Counter:
    def __init__(self):
        self.__count = 0
    def increment(self):
        self.__count += 1
    def decrement(self):        
        self.__count -= 1
    def get_count(self):
        return self.__count
    
counter = Counter()
# counter.increment()
# counter.increment()
# print(counter.get_count())  # Output: 2
# counter.decrement()
# print(counter.get_count())  # Output: 1 

# print(counter.__count) # This will raise an AttributeError because __count is a private attribute and cannot be accessed directly from outside the class
# print(counter._Counter__count) # This will print the value of __count because it uses name mangling to access the private attribute, but it is not recommended to access private attributes in this way as it breaks encapsulation and can lead to unexpected behavior.

