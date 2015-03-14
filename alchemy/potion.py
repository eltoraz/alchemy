from alchemy.reagent import Reagent

class Potion:
    # Name: short name (e.g., for display in inventory) - string
    # Description: flavor text (preferably don't just list effects) - string
    # Effects: list of positive/negative effects (incl. magnitudes where appropriate) - list of dict
    #          [{"effect": string, "magnitude": number}]
    #          TODO: separate class for effects may be useful later to 
    # Recipe: list of elements (w/ concentration thresholds) req. to craft potion - list of dict
    #         [{"element": name, "min": number, "max": number}]
    # Multiplier: (optional) multiplier for magnitude of effects - number
    #             TODO: probably want a more refined way to reflect higher/lower potion quality
    def __init__(self, name, description, effects, recipe, multiplier=1):
        self.name = name
        self.description = description
        self.effects = effects
        self.recipe = recipe
        self.multiplier = multiplier

