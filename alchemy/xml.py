"""
XML-related functions, primarily for loading assets
"""
from ast import literal_eval
import xml.etree.ElementTree as ET

from alchemy.config import assets_path
from alchemy.config import xml_namespace as ns

# XML attributes always parse as strings with this XML library, so convert numbers present to a more convenient format
# Currently supports: reagent.elements, potion.effect, potion.recipe
# TODO: catch ValueError raised if the XML attrib is malformed/invalid
def parse_xml_numbers(orig_dict):
    """Parse numbers from certain strings obtained from reading in an XML file

    Arguments:
      orig_dict (dict): dict with some numeric values, currently represented as str

    Returns:
      result (dict): original dict with numeric values converted from str -> float
    """
    result = orig_dict
    number_attribs = ['magnitude', 'duration', 'min', 'max', 'concentration']

    for key in orig_dict:
        if key in number_attribs:
            result[key] = literal_eval(orig_dict[key])

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
        desc = node.find('xmlns:description', ns).text.strip()

        # The xmlns prefix (not present in the actual XML) is needed when naming XML elements due to the way the
        # etree library handles namespaces
        xml_properties = node.find('xmlns:properties', ns).findall('xmlns:element', ns)
        props = [parse_xml_numbers(xml_prop.attrib) for xml_prop in xml_properties]

        reagents.append(Reagent(name, desc, props))
        
    return reagents

def load_potions_from_xml(filename):
    """Build a list of potions from the specified (XML) file

    Arguments:
      filename (str): name of the XML file to read from

    Returns:
      potions (list of Potion): potions parsed from the XML file
    """
    from alchemy.potion import PotionType, Potion
    potions = []
    
    for node in ET.parse(assets_path + filename).getroot():
        # parse each XML node and add to internal potions list
        name = node.get('name', 'dummy')
        desc = node.find('xmlns:description', ns).text.strip()

        type_text = node.find('xmlns:type', ns).text.strip()
        main_type = PotionType[type_text]

        xml_subtype = node.find('xmlns:subtype', ns)
        subtype = PotionType[xml_subtype.text.strip()] if xml_subtype is not None else None

        xml_effects = node.find('xmlns:effects', ns).findall('xmlns:effect', ns)
        effects = [parse_xml_numbers(xml_eff.attrib) for xml_eff in xml_effects]

        # TODO: expand for unique ingredients (right now this only works with recipes defined soley on constituent elements)
        xml_recipe_ele = node.find('xmlns:recipe', ns).findall('xmlns:element', ns)
        recipe_ele = [parse_xml_numbers(xml_ele.attrib) for xml_ele in xml_recipe_ele]
        recipe = recipe_ele

        potions.append(Potion(name, main_type, desc, effects, recipe, subtype))
        
    return potions
