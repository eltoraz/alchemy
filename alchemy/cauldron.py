'''
Do the actual mixing - even if the process doesn't use an actual cauldron
'''
from alchemy.reagent import Reagent, crops
from alchemy.potion import potions

class Cauldron:
    '''An in-progress concoction'''
    def __init__(self, reagents):
        '''reagents: list of ingredients to start the mix'''
        self.elements = {}
        self.add_ingredients(*reagents)

    def add_ingredients(self, *reagents):
        '''add the given Reagent(s) into the mix'''
        # TODO: when implemented, handle special ingredients that have unique properties
        for ingr in reagents:
            for ele in ingr.elements:
                self.elements[ele['element']] = self.elements.get(ele['element'], 0.0) + ele['concentration']

    # TODO: disallow negative `amount` or think of a good reason to allow distilling to increase element instead
    def distill(self, element, amount):
        '''remove `amount` of `element` from the cauldron
        return the actual amount removed'''
        current_amount = self.elements.get(element, 0.0)
        if current_amount <= amount:
            return self.elements.pop(element, current_amount)
        else:
            self.elements[element] = self.elements[element] - amount
            return amount

    def brew(self):
        '''combine the elements in the cauldron into a matching potion'''
        pass
