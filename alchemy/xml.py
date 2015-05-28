'''
Load data from XML
'''
from ast import literal_eval
import xml.etree.ElementTree as ET

from alchemy.config import assets_path
from alchemy.config import xml_namespace as ns

# XML attributes always parse as strings with this XML library, so convert numbers present to a more convenient format
# Currently supports: potion.effect, potion.recipe
# TODO: catch ValueError raised if the XML attrib is malformed/invalid
def parse_xml_numbers(eff_dict):
    result = eff_dict
    number_attribs = ['magnitude', 'mult', 'min', 'max']

    for key in eff_dict:
        if key in number_attribs:
            result[key] = literal_eval(eff_dict[key])

    return result

# TODO: accept multiple filenames to parse in one function call for both loading functions?
def load_reagents_from_xml(filename):
    '''Build a list of reagents fron the specified (XML) file'''
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
    '''Build a list of potions from the specified (XML) file'''
    from alchemy.potion import Potion
    potions = []
    
    for node in ET.parse(assets_path + filename).getroot():
        # parse each XML node and add to internal potions list
        name = node.get('name', 'dummy')
        desc = node.find('xmlns:description', ns).text

        # note: effects don't necessarily have a multiplier defined
        xml_effects = node.find('xmlns:effects', ns).findall('xmlns:effect', ns)
        effects = [parse_xml_numbers(xml_eff.attrib) for xml_eff in xml_effects]

        # TODO: expand for unique ingredients (right now this only works with recipes defined soley on constituent elements)
        xml_recipe_ele = node.find('xmlns:recipe', ns).findall('xmlns:element', ns)
        recipe_ele = [parse_xml_numbers(xml_ele.attrib) for xml_ele in xml_recipe_ele]
        recipe = recipe_ele

        potions.append(Potion(name, desc, effects, recipe))
        
    return potions
