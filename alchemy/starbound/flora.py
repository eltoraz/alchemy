import json

from alchemy.reagent import Reagent
from alchemy.starbound import crops as sb_crops

crops = []
conv_file = open('alchemy/starbound/flora_conversion.json', 'r')
conversions = json.load(conv_file)

for crop in sb_crops:
    new_elements = []
    for element in crop.elements:
        # catch cases where I (e.g.) pull in more assets but don't update the subtitution rules
        if element['element'] not in conversions.keys():
            new_elements.append(element)
            continue

        # inconsistencies in fields where some of the SB items don't have magnitude associated
        # with the effect
        subst = {'element': conversions[element['element']], 'duration': element['duration']}
        if 'concentration' in element.keys():
            subst['concentration'] = element['concentration']

        new_elements.append(subst)

    crops.append(Reagent(name=crop.name, description=crop.description, elements=new_elements))

