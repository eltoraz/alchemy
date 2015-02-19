'''
An alchemy ingredient
'''
class Reagent:
    # Name: self-explanatory - string
    # Description: short flavor text - string
    # Elements: affinities/attributes of the reagent that determine properties - dict {element (string): strength (number)}
    def __init__(self, name='', description='', elements={}):
        self.name = name
        self.description = description
        self.elements = elements

    def __repr__(self):
        return {'name': self.name, 'description': self.description, 'elements': self.elements}.__str__()

    def __str__(self):
        return __repr__(self)

