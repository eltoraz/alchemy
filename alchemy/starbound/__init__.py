'''
Pull relevant data from Starbound crop assets.
'''
import json

from alchemy.config import assets_path
from alchemy.reagent import Reagent

# format of effects file: list of effects (strings)
effects_file = open(assets_path+'starbound_effects.json', 'r')
effects = json.load(effects_file)

# format of crops file: list of crops (dict containing name (string), description (string), effects (dict))
crops_file = open(assets_path+'starbound_crops.json', 'r')
serialized_crops = json.load(crops_file)
crops = []
for crop in serialized_crops:
    crops.append(Reagent(name=crop['name'], description=crop['description'], elements=crop['elements']))

