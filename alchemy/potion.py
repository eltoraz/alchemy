"""A potion (generally speaking), along with related functions
"""
from collections import namedtuple
from enum import Enum
import xml.etree.ElementTree as ET

from alchemy.config import assets_path
from alchemy.config import xml_namespace as ns
from alchemy.item import Item
from alchemy.util import eval_xml_numbers

class PotionType(Enum):
    """All the possible classifications for potions

    Every potion needs a main type (id < 10), but some may have
    subtypes (id >= 10) for easier categorization. The main type
    relates to the potion's physical state or application method, while
    the subtype provides more context (like whether it's malignant or
    otherwise unique).
    """
    potion = 1
    salve = 2
    volatile = 3
    vapor = 4

    poison = 10
    explosive = 11
    corrosive = 12

# TODO: consider a separate class for effects instead of passing dicts
#       around
# TODO: support recipes that call for specific ingredients alongside
#       element requirements
class Potion(Item):
    """A potion
    
    Arguments:
      name (str): display name
      main_type (PotionType): category the potion falls under
      desc (str): flavor text
      effects (list of dict): positive/negative effects (including
                              magnitudes/duration where appropriate)
                              {"effect": str, "magnitude": float,
                              "duration": float}
      recipe (list of dict): elements (w/ concentration thresholds)
                             required to craft potion
                             {"element": str, "min": float,
                             "max": float}
      subtype (PotionType): additional (optional) classification for
                            the potion; None if not specified

    Attributes:
      name (str): display name
      main_type (PotionType): category the potion falls under
      description (str): flavor text (preferably more than just a list
                         of effects)
      effects (list of dict): effects of applying the potion
                              {"effect": str, "magnitude": float,
                              "duration": float}
      recipe (list of dict): ingredients needed to craft potion (either
                             specific ones or required elements w/
                             concentration thresholds)
                             {"element": str, "min": float,
                             "max": float}
      subtype (PotionType): additional (optional) classification for
                            the potion; None if not specified
    """
    def __init__(self, name, main_type, desc, effects, recipe, subtype=None):
        super().__init__(name, desc)
        self.main_type = main_type
        self.effects = effects
        self.recipe = recipe
        self.subtype = subtype

    def __repr__(self):
        dict_form = {'name': self.name, 'type': self.main_type.name,
                     'description': self.description, 'effects': self.effects,
                     'recipe': self.recipe}
        if self.subtype:
            dict_form['subtype'] = self.subtype.name

        return dict_form.__str__()

    def __str__(self):
        return self.__repr__()

# TODO: define a find/filter function to get specific (unordered)
#       entries from the potions list (perhaps extend get_matches?)

#----------------------------------------------------------------------
# Load potions from XML
def load_potions_from_xml(filename):
    """Build a list of potions from the specified (XML) file

    Arguments:
      filename (str): name of the XML file to read from

    Returns:
      potions (list of Potion): potions parsed from the XML file
    """
    potions = []
    
    for node in ET.parse(assets_path + filename).getroot():
        # parse each XML node and add to internal potions list
        name = node.get('name', 'dummy')
        desc = node.find('xmlns:description', ns).text.strip()

        type_text = node.find('xmlns:type', ns).text.strip()
        main_type = PotionType[type_text]

        xml_subtype = node.find('xmlns:subtype', ns)
        subtype = PotionType[xml_subtype.text.strip()] \
                    if xml_subtype is not None else None

        xml_effects_block = node.find('xmlns:effects', ns)
        xml_effects = xml_effects_block.findall('xmlns:effect', ns)
        effects = [eval_xml_numbers(xml_eff.attrib)
                   for xml_eff in xml_effects]

        # TODO: expand for unique ingredients (as opposed to just
        #       combinations of elements)
        xml_recipe_block = node.find('xmlns:recipe', ns)
        xml_recipe_ele = xml_recipe_block.findall('xmlns:element', ns)
        recipe_ele = [eval_xml_numbers(xml_ele.attrib)
                      for xml_ele in xml_recipe_ele]
        recipe = recipe_ele

        potions.append(Potion(name, main_type, desc, effects, recipe,
                              subtype))
        
    return potions

potions = load_potions_from_xml('potions.xml')

# TODO: find a more efficient way to find matches
# TODO: adapt for special properties/ingredient requirements in recipe
#       once that's implemented
def get_matches(elements, potion_list=potions):
    """Return all potions from the potions list that can be mixed with
    the provided ingredients.

    Arguments:
      elements (dict): mapping of elements -> concentrations to test
                       against potion recipes
      potion_list (list of Potion): list of potions to search
                                    (defaults to module's global list)

    Returns:
      results (list of Potion): potions whose recipes match the
                                ingredients ([] if no matches)
    """
    element_range = namedtuple('element_range', 'min max')
    elements_set = set(elements.keys())

    def check_match(potion):
        """Helper function: check whether the elements present fit the
        minimum requirements for the recipe of the given potion.

        Arguments:
          potion: a Potion

        Returns:
          True: if all elements in potion's recipe are present in the
                elements passed into the caller
          False: otherwise
        """
        # converting min/max to a tuple in this dict for use later
        recipe_elements = {ele['element']: element_range(ele['min'],
                           ele['max']) for ele in potion.recipe}

        # check that the elements in the recipe form a subset of the
        # provided set, and that the concentration is at least the
        # minimum required (leave checking the max. tolerated to the
        # caller)
        if (set(recipe_elements.keys()) <= elements_set and
            all([elements[ele] >= recipe_elements[ele].min for
                 ele in recipe_elements.keys()])):
            return True
        else:
            return False

    results = [potion for potion in potions if check_match(potion)]

    return results
