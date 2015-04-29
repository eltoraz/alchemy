import xml.etree.ElementTree as ET

from alchemy.config import assets_path
from alchemy.reagent import Reagent

class Potion:
    # Name: short name (e.g., for display in inventory) - string
    # Description: flavor text (preferably don't just list effects) - string
    # Effects: list of positive/negative effects (incl. magnitudes where appropriate) - list of dict
    #          [{"effect": string, "magnitude": number, "multiplier": number}]
    #          TODO: separate class for effects may be useful later to 
    # Recipe: list of elements (w/ concentration thresholds) req. to craft potion - list of dict
    #         [{"element": name, "min": number, "max": number}]
    #         TODO: support potions that require specific ingredients in addition to certain elements
    # TODO: may want a more refined way to reflect potion quality than a multiplier on each effect
    def __init__(self, name, description, effects, recipe):
        self.name = name
        self.description = description
        self.effects = effects
        self.recipe = recipe

    def from_dict(potion_dict):
        '''Assuming the passed dict is the correct format w/ all the necessary fields'''
        return Potion(potion_dict['name'], potion_dict['description'],
                      potion_dict['effects'], potion_dict['recipe'])

potions_list = []

xml_tree = ET.parse(assets_path+'potions.xml')
xml_root = xml_tree.getroot()

for child in xml_root:
    # parse each XML node and add to internal potions list
    name = child.get('name', '')
    desc = child.find('description').text
    xml_effects = child.find('effects').findall('effect')
    effects = [{'effect': xml_eff.get('type'), 'magnitude': xml_eff.get('magnitude'), 'multiplier': xml_eff.get('mult', 1.0)}
               for xml_eff in xml_effects]
    xml_recipe = child.find('recipe').findall('ingredient')
    recipe = [{'element': xml_ingr.get('element'), 'min': xml_ingr.get('min'), 'max': xml_ingr.get('max')}
              for xml_ingr in xml_recipe]
    potions_list.append(Potion(name, desc, effects,recipe))

