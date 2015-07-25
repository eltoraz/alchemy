"""
An alchemy ingredient
"""
import xml.etree.ElementTree as ET

from alchemy.config import assets_path
from alchemy.config import xml_namespace as ns
from alchemy.item import Item
from alchemy.util import eval_xml_numbers

class Reagent(Item):
    """An item/object/etc. that can be used in an alchemical concoction

    Arguments:
      name (str): display name
      description (str): short flavor text
      elements (list of dict): affinities of the reagent
                               [{"element": string,
                                 "concentration": number}]
    """
    def __init__(self, name, desc, elements):
        super().__init__(name, desc)
        self.elements = elements

    def __repr__(self):
        return {'name': self.name, 'description': self.description,
                'elements': self.elements}.__str__()

    def __str__(self):
        return self.__repr__()

#----------------------------------------------------------------------
# Load reagents from XML
# TODO: accept multiple filenames to parse in one function call?
def load_reagents_from_xml(filename):
    """Build a list of reagents fron the specified (XML) file

    Arguments:
      filename (str): name of the XML file to read from

    Returns:
      reagents (list of Reagent): reagents parsed from the XML file
    """
    reagents = []
    
    for node in ET.parse(assets_path + filename).getroot():
        name = node.get('name', 'dummy')
        desc = node.find('xmlns:description', ns).text
        # description may be not be present
        if desc:                                        
            desc = desc.strip()

        # The xmlns prefix (not present in the actual XML) is needed
        # when naming XML elements due to the way the etree library
        # handles namespaces
        xml_properties_block = node.find('xmlns:properties', ns)
        xml_properties = xml_properties_block.findall('xmlns:element', ns)
        props = [eval_xml_numbers(xml_prop.attrib)
                 for xml_prop in xml_properties]

        reagents.append(Reagent(name, desc, props))
        
    return reagents

crops = load_reagents_from_xml('crops.xml')

reagents = crops
