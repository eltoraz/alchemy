"""A (metaphorical) cauldron for combining reagents into a potion
"""
import alchemy.potion

class Cauldron:
    """A cauldron to hold and manipulate potion ingredients

    Arguments:
      reagents (list of Reagent): Cauldron's initial ingredients
    """
    def __init__(self, reagents=[]):
        self.elements = {}
        self.add_ingredients(*reagents)

        self.update()

    def add_ingredients(self, *reagents):
        """Add ingredients to the mix.

        Specifically, add the ingredient's elements.

        Arguments:
          reagents (Reagent): ingredients to throw in the cauldron
        """
        # TODO: when implemented, handle special ingredients that have
        #       unique properties
        for ingr in reagents:
            for ele in ingr.elements:
                ele_type = ele['element']
                self.elements[ele_type] = (self.elements.get(ele_type, 0.0) +
                                           ele['concentration'])

        self.update()

    def distill(self, element, amount):
        """Remove a certain amount of an element from the Cauldron and
        return the actual amount distilled.

        Raises AssertionException if amount is negative (i.e., trying
        to use this method to increase the concentration of an element
        in the Cauldron).

        If the specified element is not present in the mix, the
        Cauldron is not changed.

        Arguments:
          element (str): element to be reduced/removed
          amount (float): concentration of the element to attempt
                          to remove

        Returns:
          amount or current_amount (float): actual amount removed from
                                            Cauldron (0 if not present)
        """
        # TODO: validate the element, perhaps?
        assert amount >= 0, \
                "Distilling cannot increase the element's concentration!"

        current_amount = self.elements.get(element, 0)

        if current_amount <= amount:
            return self.elements.pop(element, current_amount)
        else:
            self.elements[element] = self.elements[element] - amount
            return amount

        self.update()

    def update(self):
        """Modify the internal state of the cauldron based on recent
        changes. Notably, update the perspective recipe list after the
        contents of the Cauldon changes.
        """
        self.possible_results = alchemy.potion.get_matches(self.elements)

    def empty(self):
        """Empty the Cauldron of all its contents.
        """
        self.elements = {}
        self.update()

    # TODO: remove print statements when the game handles the results
    #       elsewhere
    # TODO: verify that no extra ingredients are in the cauldron?
    def brew(self):
        """Attempt to combine the elements in the cauldron into a
        matching potion.

        If there's any ambiguity (i.e., multiple recipes fit the
        contents of the Cauldron), let the player know their options
        (ex., remove elements to narrow possibilities).

        Note: this operation clears everything from the Cauldon if
        successful!

        Returns:
          result (Potion): a potion whose recipe matches the contents
                           of the Cauldron, OR
          possible_results (list of Potion): list of potions that can
                                             be created, OR
          None: if the contents of the Cauldron don't match a potion in
                the list
        """
        # possible_results contains potions whose minimum requirements
        # are met, so we need to make sure the max bound is satisfied
        # when actually trying to make the brew here
        range_check = [False]
        if len(self.possible_results) > 0:
            range_check = [self.elements[ele['element']] <= ele['max']
                           for ele in self.possible_results[0].recipe]

        if len(self.possible_results) == 1 and all(range_check):
            ele_list = list(self.elements.keys())
            result = self.possible_results[0]

            print('Brew successful! Created ', result.name, ' from ',
                  sep='', end='')
            for ele in ele_list[0:-1]:
                print(self.elements[ele], ' units of ', ele, ', ',
                      sep='', end='')
            print('and ', self.elements[ele_list[-1]], ' units of ',
                  ele_list[-1], '.', sep='')

            self.empty()
            return result
        elif len(self.possible_results) > 0:
            print('Progress! The following potions are possible:')
            for potion in self.possible_results:
                print(' -', potion.name)
            return self.possible_results
        else:
            print("Oops, that's not a winning combination!",
                  "Better try again...")
            return None
