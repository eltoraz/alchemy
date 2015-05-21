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
