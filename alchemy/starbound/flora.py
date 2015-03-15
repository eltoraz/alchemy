import json

import jsonpatch

from alchemy.config import assets_path
from alchemy.reagent import Reagent
from alchemy.starbound import crops as sb_crops
from alchemy.starbound.convert_sb_assets import persist_crops

# TODO: check if flora_crops.json was more recently modified than crops.json;
#       if so, just read from that

crops = []
conv_file = open(assets_path+'flora_conversion.json', 'r')
conversions = json.load(conv_file)

patch_file = open(assets_path+'flora_crops_patch.json', 'r')
patches = json.load(patch_file)

# go through and subsitute flora elements for SB effects, and add a few manually via the patch file
for crop in sb_crops:
    new_elements = []
    for element in crop.elements:
        # in cases where I (e.g.) pull in more assets but don't update the subtitution rules, toss the effect
        if element['element'] not in conversions.keys():
            continue

        # Calculate a new concentration based on the duration and magnitude of SB effects
        # Based on the numbers a logarithmic scale (a la pH) fits, but need to figure out what it measures
        # Some don't need a magnitude defined and so associated food items won't have it
        # (there shouldn't be many of these)
        sb_dur = element['duration']
        sb_con = 0.5
        if 'concentration' in element.keys():
            sb_con = element['concentration'] / 100
        concentration = sb_dur * sb_con

        subst = {'element': conversions[element['element']], 'concentration': concentration}

        new_elements.append(subst)

    # sub in the flora elements, and patch in corrections/additions
    new_elements = sorted(new_elements, key=lambda ele: ele['element'])
    subbed_crop = Reagent(name=crop.name, description=crop.description, elements=new_elements)
    try:
        patched_dict = jsonpatch.apply_patch(subbed_crop.__dict__, patches[crop.name])
        patched_crop = Reagent(name=patched_dict['name'],
                               description=patched_dict['description'],
                               elements=patched_dict['elements'])
    except KeyError:
        patched_crop = subbed_crop

    crops.append(patched_crop)

def persist_changes():
    '''Save the Starbound crops with element substitutions'''
    persist_crops(crops, assets_path+'flora_crops.json')

