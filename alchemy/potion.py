'''
A potion (generally speaking)
'''
import xml.etree.ElementTree as ET

from alchemy.config import assets_path
from alchemy.config import xml_namespace as ns
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

potions = []

# As in reagent.py, the xmlns: prefix is required (the alternative is writing out the full namespace)
for node in ET.parse(assets_path + 'potions.xml').getroot():
    # parse each XML node and add to internal potions list
    name = node.get('name', 'dummy')
    desc = node.find('xmlns:description', ns).text

    # note: effects don't necessarily have a multiplier defined
    xml_effects = node.find('xmlns:effects', ns).findall('xmlns:effect', ns)
    effects = [{'effect': xml_eff.find('xmlns:type', ns).text,
                'magnitude': xml_eff.find('xmlns:magnitude', ns).text,
                'multiplier': xml_eff.find('xmlns:mult', ns).text if xml_eff.find('xmlns:mult', ns) is not None else 1.0}
               for xml_eff in xml_effects]

    # TODO: expand for unique ingredients (right now this only works with recipes defined soley on constituent elements)
    xml_recipe = node.find('xmlns:recipe', ns).findall('xmlns:ingredient', ns)
    recipe = []
    for xml_ingr in xml_recipe:
        xml_ele = xml_ingr.find('xmlns:element', ns)
        recipe.append({'element': xml_ele.find('xmlns:type', ns).text,
                    'min': xml_ele.find('xmlns:min', ns).text,
                    'max': xml_ele.find('xmlns:max', ns).text})

    potions.append(Potion(name, desc, effects,recipe))

