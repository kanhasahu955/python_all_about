# class HtmlDocument:
#     pass

# # create instance of the class
# doc1 = HtmlDocument()
# print(doc1)  # Output: <__main__.HtmlDocument object at 0x7f8b8c2e5d30>
# print(type(doc1))  # Output: <class '__main__.HtmlDocument'>
# print(isinstance(doc1, HtmlDocument))  # Output: True
# print(HtmlDocument.__name__)  # Output: HtmlDocument (the name of the class)
# print(type(HtmlDocument))  # Output: <class 'type'> (HtmlDocument is a class, which is an instance of the type class)
# print(isinstance(HtmlDocument, type))  # Output: True (HtmlDocument is an instance of the type class)


# Class variables are bound to the class. They’re shared by all instances of that class.
# class HtmlDocument:
#     version = "HTML5"  # class variable
#     doctype = "<!DOCTYPE html>"  # class variable


# print(HtmlDocument.version)  # Output: HTML5
# print(HtmlDocument.doctype)  # Output: <!DOCTYPE html>
# # print(HtmlDocument.name) # Output: AttributeError: type object 'HtmlDocument' has no attribute 'name' (since 'name' is not defined as a class variable)
# print(HtmlDocument.__dict__)  # Output: {'__module__': '__main__', 'version': 'HTML5', 'doctype': '<!DOCTYPE html>', '__dict__': <attribute '__dict__' of 'HtmlDocument' objects>, '__weakref__': <attribute '__weakref__' of 'HtmlDocument' objects>, '__doc__': None} (shows the class variables and other attributes of the class)

# print(getattr(HtmlDocument, 'version'))  # Output: HTML5 (using getattr to access class variable)
# print(getattr(HtmlDocument, 'doctype'))  # Output: <!DOCTYPE html> (using getattr to access class variable)
# print(hasattr(HtmlDocument, 'version'))  # Output: True (checking if class variable 'version' exists)
# print(hasattr(HtmlDocument, 'name'))  # Output: False (checking if class variable 'name' exists)
# print(getattr(HtmlDocument, 'name', 'Not Found'))  # Output: Not Found (using getattr with default value for non-existent class variable)



# set values for class variables
class HtmlDocument:
    version = "HTML5"  # class variable
    doctype = "<!DOCTYPE html>"  # class variable
    def __init__(self, title):
        self.title = title  # instance variable
doc1 = HtmlDocument("My Web Page")
print(doc1.title)  # Output: My Web Page (accessing instance variable)
print(doc1.version)  # Output: HTML5 (accessing class variable through instance)
print(doc1.doctype)  # Output: <!DOCTYPE html> (accessing class variable    through instance)
print(HtmlDocument.version)  # Output: HTML5 (accessing class variable directly from the    class)
print(HtmlDocument.doctype)  # Output: <!DOCTYPE html> (accessing class variable
