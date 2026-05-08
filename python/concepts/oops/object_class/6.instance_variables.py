from pprint import pprint

class HtmlDocument:
    version = 5
    type = "text/html"

html_doc = HtmlDocument()
print(type(HtmlDocument))  # Output: <class 'type'> (HtmlDocument is a class, which is an instance of the type class)
print(type(html_doc))  # Output: <class '__main__.HtmlDocument'> (html_doc is an instance of the HtmlDocument class)

print(html_doc.version)  # Output: 5 (html_doc can access the class variable version)
print(html_doc.type)  # Output: text/html (html_doc can access the class variable type)

pprint(HtmlDocument.__dict__)  # Output: {'__module__': '__main__', 'version': 5, 'type': 'text/html', '__dict__': <attribute '__dict__' of 'HtmlDocument' objects>, '__weakref__': <attribute '__weakref__' of 'HtmlDocument' objects>, '__doc__': None} (the class variables version and type are stored in the class's __dict__)
pprint(html_doc.__dict__)  # Output: {} (the instance html_doc does not have its own __dict__ since it does not have any instance variables)

html_doc.version = 6  # This creates an instance variable version for html_doc, which shadows the class variable version
print(html_doc.version)  # Output: 6 (html_doc now accesses the instance variable version instead of the class variable version)
print(HtmlDocument.version)  # Output: 5 (HtmlDocument.version accesses the class variable version)

HtmlDocument.version = 7  # This changes the class variable version for all instances of HtmlDocument that do not have their own instance variable version
print(html_doc.version)  # Output: 6 (html_doc still accesses its own instance variable version)