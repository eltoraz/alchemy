'''
An alchemy ingredient
'''
class Reagent:
    # Name: self-explanatory - string
    # Description: short flavor text - string
    # Elements: affinities/attributes of the reagent that determine properties - list of dict
    #           [{"element": string, "concentration": number}]
    def __init__(self, name='', description='', elements=[]):
        self.name = name
        self.description = description
        self.elements = elements

    def __repr__(self):
        return {'name': self.name, 'description': self.description, 'elements': self.elements}.__str__()

    def __str__(self):
        return self.__repr__()

# note: alchemy.xml needs the Reagent class to be defined before it can be imported
import alchemy.xml

crops = alchemy.xml.load_reagents_from_xml('crops.xml')
