'''
An alchemy ingredient
'''
class Reagent:
    # Name: self-explanatory - string
    # Description: short flavor text - string
    # Essences: properties that react when mixing - dict {essences (string): strength (number)}
    def __init__(self, name, description, essences={}):
        self.name = name
        self.description = description
        self.essences = essences

    def __repr__(self):
        return {'name': self.name, 'description': self.description, 'essences': self.essences}.__str__()

    def __str__(self):
        return __repr__(self)

