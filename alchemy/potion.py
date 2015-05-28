'''
A potion (generally speaking)
'''
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

    def __repr__(self):
        return {'name': self.name, 'description': self.description,
                'effects': self.effects, 'recipe': self.recipe}.__str__()

    def __str__(self):
        return self.__repr__()

    def from_dict(potion_dict):
        '''Assuming the passed dict is the correct format w/ all the necessary fields'''
        return Potion(potion_dict['name'], potion_dict['description'],
                      potion_dict['effects'], potion_dict['recipe'])

# note: alchemy.xml needs the Potion class to be defined before it can be imported
import alchemy.xml

potions = alchemy.xml.load_potions_from_xml('potions.xml')

# TODO: maybe check whether the potion requirements are a subset of what's in the cauldron, but make
#       sure there isn't any ambiguity (from multiple potions with similar recipes)
# TODO: find a more efficient way to find matches
# TODO: adapt for special properties/ingredient requirements in recipe once that's implemented
def get_match(elements):
    '''return one potion from the list that matches the provided ingredients
    specifically, the types of elements must match exactly, with concentrations between the limits in the recipe
    if no match, return None'''
    elements_set = set(elements.keys())
    for potion in potions:
        # first step: check whether the required elements (and no additional ones) are present
        # converting min/max to a tuple in this dict for use later
        recipe_elements = {ele['element']: (ele['min'], ele['max']) for ele in potion.recipe}
        if elements_set != set(recipe_elements.keys()):
            continue

        # if the ingredients match the recipe, just make sure they're between the specified min & max
        if all([elements[ele] >= recipe_elements[ele][0] and
                elements[ele] <= recipe_elements[ele][1] for
                ele in elements_set]):
            return potion

    # fallback (no match)
    return None
