"""
An alchemy ingredient
"""
class Reagent:
    """An item/object/etc. that can be used in an alchemical concoction

    Arguments:
      name (str): display name
      description (str): short flavor text
      elements (list of dict): affinities of the reagent
                               [{"element": string, "concentration": number}]
    """
    def __init__(self, name, description, elements):
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
