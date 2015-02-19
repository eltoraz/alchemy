'''
Pull relevant data from Starbound crop assets.
'''
import json

from alchemy.reagent import Reagent

# format of effects file: list of effects (strings)
effects_file = open('alchemy/starbound/effects.json', 'r')
effect_list = json.load(effects_file)

# format of crops file: list of crops (dict containing name (string), description (string), effects (dict))
crops_file = open('alchemy/starbound/crops.json', 'r')
serialized_crops = json.load(crops_file)
crops = []
for crop in serialized_crops:
    crops.append(Reagent(name=crop['name'], description=crop['description'], elements=crop['elements']))

