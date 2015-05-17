'''
An alchemy ingredient
'''
import xml.etree.ElementTree as ET

from alchemy.config import assets_path
from alchemy.config import xml_namespace as ns

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

crops = []

# The xmlns prefix (not present in the actual XML) is needed below in find() due to quirks in the etree library
for node in ET.parse(assets_path + 'crops.xml').getroot():
    name = node.get('name', 'dummy')
    desc = node.find('xmlns:description', ns).text

    xml_elements = node.find('xmlns:properties', ns).findall('xmlns:element', ns)
    props = [{'element': xml_ele.get('type'), 'concentration': xml_ele.get('concentration')}
             for xml_ele in xml_elements]

    crops.append(Reagent(name, desc, props))

