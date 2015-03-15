'''
Standalone script to build/rebuild crop & effect lists from Starbound assets
'''
import re
import json
from os import listdir

from alchemy.config import assets_path
from alchemy.reagent import Reagent

sb_assets_path = 'alchemy/starbound/assets/'
crops = []
effect_list = []

# Starbound food effect internal names are pretty regular, composed of two parts, the effect itself and magnitude,
# though some don't specify magnitude (ex. 'thorns'), in which case the magnitude group in the regex will be ''
effect_magnitude_re = re.compile('^\D+(\d*)')

for crop_filename in listdir(sb_assets_path):
    crop_file = open(sb_assets_path + crop_filename)
    crop_json = json.load(crop_file)
    name = crop_json['shortdescription']
    desc = crop_json['description']

    effects = []

    # note: some crops in 'assets/items/generic/produce/' aren't consumable themselves (hence don't have 'effects' field)
    if 'effects' in crop_json and type(crop_json['effects'][0][0]) is dict:
        for effect in crop_json['effects'][0]:
            # don't care about 'wellfed' debuff, so don't process it at all
            if effect['effect'] == 'wellfed':
                continue

            # some SB effects have a magnitude in the effect name (ex. 'foodheal10') that feeds into the script along
            # the duration; I want to preserve that for now to possibly determine element concentration
            # ex. more potent/longer-lasting effects result from higher concentration of the corresponding element
            magnitude = effect_magnitude_re.match(effect['effect']).group(1)
            if magnitude:
                effects.append({'element': effect['effect'], 'concentration': int(magnitude), 'duration': effect['duration']})
            else:
                effects.append({'element': effect['effect'], 'duration': effect['duration']})

            if effect['effect'] not in effect_list:
                effect_list.append(effect['effect'])

    crops.append(Reagent(name, desc, effects))

def persist_crops(crops, file_path):
    '''Save the given list of crops (Reagents) to the specified file as JSON'''
    crops_file = open(file_path, 'w')
    serialized_crops = []
    for crop in sorted(crops, key=lambda crop: crop.name):
        serialized_crops.append(crop.__dict__)
    json.dump(serialized_crops, crops_file, indent=2, sort_keys=True)
    crops_file.close()
    
# write the effects and crops to a file so they don't have to be rebuilt every time
effects_file = open(assets_path+'starbound_effects.json', 'w')
json.dump(effect_list, effects_file, indent=2, sort_keys=True)
effects_file.close()
persist_crops(crops, assets_path+'starbound_crops.json')

