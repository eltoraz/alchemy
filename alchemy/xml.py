"""
XML-related functions, primarily for loading assets
"""
from ast import literal_eval
import xml.etree.ElementTree as ET

from alchemy.config import assets_path
from alchemy.config import xml_namespace as ns
from alchemy.potion import PotionType

# XML attributes always parse as strings with this XML library, so convert numbers present to a more convenient format
# Currently supports: potion.effect, potion.recipe
# TODO: catch ValueError raised if the XML attrib is malformed/invalid
def parse_xml_numbers(eff_dict):
    """Parse numbers from certain strings obtained from reading in an XML file

    Arguments:
      eff_dict (dict): dict with some numeric values, currently represented as str

    Returns:
      result (dict): original dict with numeric values converted from str -> float
    """
    result = eff_dict
    number_attribs = ['magnitude', 'min', 'max']

    for key in eff_dict:
        if key in number_attribs:
            result[key] = literal_eval(eff_dict[key])

    return result

# TODO: accept multiple filenames to parse in one function call for both loading functions?
def load_reagents_from_xml(filename):
    """Build a list of reagents fron the specified (XML) file

    Arguments:
      filename (str): name of the XML file to read from

    Returns:
      reagents (list of Reagent): reagents parsed from the XML file
    """
    from alchemy.reagent import Reagent
    reagents = []
    
    for node in ET.parse(assets_path + filename).getroot():
        name = node.get('name', 'dummy')
        desc = node.find('xmlns:description', ns).text

        # The xmlns prefix (not present in the actual XML) is needed when naming XML elements due to the way the
        # etree library handles namespaces
        xml_elements = node.find('xmlns:properties', ns).findall('xmlns:element', ns)
        props = [{'element': xml_ele.get('element'),
                'concentration': literal_eval(xml_ele.get('concentration'))}
                for xml_ele in xml_elements]

        reagents.append(Reagent(name, desc, props))
        
    return reagents

def load_potions_from_xml(filename):
    """Build a list of potions from the specified (XML) file

    Arguments:
      filename (str): name of the XML file to read from

    Returns:
      potions (list of Potion): potions parsed from the XML file
    """
    from alchemy.potion import Potion
    potions = []
    
    for node in ET.parse(assets_path + filename).getroot():
        # parse each XML node and add to internal potions list
        name = node.get('name', 'dummy')
        desc = node.find('xmlns:description', ns).text

        cat_text = node.find('xmlns:category', ns).text
        cat = PotionType[cat_text]

        xml_effects = node.find('xmlns:effects', ns).findall('xmlns:effect', ns)
        effects = [parse_xml_numbers(xml_eff.attrib) for xml_eff in xml_effects]

        # TODO: expand for unique ingredients (right now this only works with recipes defined soley on constituent elements)
        xml_recipe_ele = node.find('xmlns:recipe', ns).findall('xmlns:element', ns)
        recipe_ele = [parse_xml_numbers(xml_ele.attrib) for xml_ele in xml_recipe_ele]
        recipe = recipe_ele

        potions.append(Potion(name, cat, desc, effects, recipe))
        
    return potions
