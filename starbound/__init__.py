'''
Pull relevant data from Starbound crop assets.
'''
import json
from os import listdir

from alchemy.reagent import Reagent

assets_path = 'alchemy/starbound/assets/'
crops = []
effect_list = []

'''
TODO:
- figure out appropriate elements to replace SB effects (also conversion of SB effect
  strength/duration -> element strength/purity/concentration/whatever)
'''

for crop_filename in listdir(assets_path):
    crop_file = open(assets_path + crop_filename)
    crop_json = json.load(crop_file)
    name = crop_json['shortdescription']
    desc = crop_json['description']

    effects = {}

    # map SB produce effects to essences for now
    # note: some crops in 'assets/items/generic/produce/' aren't consumable themselves (hence don't have 'effects' field)
    if 'effects' in crop_json and type(crop_json['effects'][0][0]) is dict:
        for effect in crop_json['effects'][0]:
            effects[effect['effect']] = effect['duration']
            if effect['effect'] not in effect_list:
                effect_list.append(effect['effect'])

    # don't really care about well fed debuff
    effects.pop('wellfed', '')

    crops.append(Reagent(name, desc, effects))

if 'wellfed' in effect_list:
    effect_list.remove('wellfed')

