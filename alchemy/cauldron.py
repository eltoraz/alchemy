'''
Do the actual mixing - even if the process doesn't use an actual cauldron!
'''
from alchemy.reagent import Reagent, crops
from alchemy.potion import potions

class Cauldron:
    '''An in-progress concoction'''
    def __init__(self, *reagents):
        '''reagents: individual ingredients to start the mix
        '''
        self.elements = {}

        for ingr in reagents:
            for ele in ingr.elements:
                # TODO: need to convert reagents XML attributes -> elements, write schema defining numeric datatype
                self.elements[ele['element']] = self.elements.get(ele['element'], 0.0) + ele['concentration']
