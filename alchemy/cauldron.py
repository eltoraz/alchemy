'''
Do the actual mixing - even if the process doesn't use an actual cauldron
'''
import alchemy.potion

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

    def distill(self, element, amount):
        '''remove `amount` of `element` from the cauldron
        NOTE: amount must be nonnegative
        return the actual amount removed
        if the element is not present in the cauldron, the elements dict is unaffected'''
        assert amount >= 0, 'Distilling cannot increase the concentration of an element!'

        current_amount = self.elements.get(element, 0.0)

        if current_amount <= amount:
            return self.elements.pop(element, current_amount)
        else:
            self.elements[element] = self.elements[element] - amount
            return amount

    def brew(self):
        '''attempt to combine the elements in the cauldron into a matching potion
        if successful, empty the cauldron and return the result
        otherwise, just print a failure message'''
        result = alchemy.potion.get_match(self.elements)
        if result is not None:
            ele_list = list(self.elements.keys())
            print('Brew successful! Created ', result.name, ' from ', sep='', end='')
            for ele in ele_list[0:-1]:
                print(self.elements[ele], ' units of ', ele, ', ', sep='', end='')
            print('and ', self.elements[ele_list[-1]], ' units of ', ele_list[-1], '.', sep='')
            self.elements = {}
        else:
            print('Oops, that\'s not a winning combination! Better try again...')

        return result
