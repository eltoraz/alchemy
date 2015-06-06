"""
A potion (generally speaking), along with related functions
"""
from enum import Enum

class PotionType(Enum):
    """Various types of potion available
    """
    potion = 1
    salve = 2
    volatile = 3
    vapor = 4

# TODO: consider a separate class for effects instead of passing dicts around
# TODO: support recipes that call for specific ingredients alongside element requirements
class Potion:
    """A potion
    
    Arguments:
      name (str): display name
      cat (PotionType): category the potion falls under
      desc (str): flavor text
      effects (list of dict): positive/negative effects (incl. magnitudes where appropriate)
                              {"effect": string, "magnitude": number}
      recipe (list of dict): elements (w/ concentration thresholds) required to craft potion
                             {"element": name, "min": number, "max": number}

    Attributes:
      name (str): display name
      category (PotionType): category the potion falls under
      description (str): flavor text (preferably more than just a list of effects)
      effects (list of dict): effects of applying the potion
                              {"effect": string, "magnitude": number}
      recipe (list of dict): ingredients needed to craft potion (either specific ones or
                             required elements w/ concentration thresholds)
                             {"element": name, "min": number, "max": number}
    """
    def __init__(self, name, cat, desc, effects, recipe):
        self.name = name
        self.category = cat
        self.description = desc
        self.effects = effects
        self.recipe = recipe

    def __repr__(self):
        return {'name': self.name, 'type': self.category.name, 'description': self.description,
                'effects': self.effects, 'recipe': self.recipe}.__str__()

    def __str__(self):
        return self.__repr__()

# TODO: maybe check whether the potion requirements are a subset of what's in the cauldron, but make
#       sure there isn't any ambiguity (from multiple potions with similar recipes)
# TODO: find a more efficient way to find matches
# TODO: adapt for special properties/ingredient requirements in recipe once that's implemented
def get_match(elements):
    """Return the first potion from the potions list that matches the provided ingredients.

    Arguments:
      elements (dict): mapping of elements -> concentrations to test against potion recipes

    Returns:
      potion (Potion): potion whose recipe matches the ingredients, OR
      None: if the elements/concentrations don't match a recipe
    """
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

# ------------------------------------------------------
# Load potions from XML
# note: alchemy.xml module needs the Potion class to be defined before it can be imported
import alchemy.xml

potions = alchemy.xml.load_potions_from_xml('potions.xml')
