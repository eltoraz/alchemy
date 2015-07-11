"""
A (metaphorical) cauldron for combining reagents into a potion
"""
import alchemy.potion

class Cauldron:
    """A cauldron to hold and manipulate potion ingredients

    Arguments:
      reagents (list of Reagent): ingredients to add to the cauldron to start out
    """
    def __init__(self, reagents):
        self.elements = {}
        self.add_ingredients(*reagents)

    def add_ingredients(self, *reagents):
        """Add ingredients to the mix.

        Specifically, add the ingredient's elements.

        Arguments:
          reagents (Reagent): ingredients to throw in the cauldron
        """
        # TODO: when implemented, handle special ingredients that have unique properties
        for ingr in reagents:
            for ele in ingr.elements:
                self.elements[ele['element']] = self.elements.get(ele['element'], 0.0) + ele['concentration']

    def distill(self, element, amount):
        """Remove a certain amount of an element from the Cauldron and return the actual amount distilled.

        Raises AssertionException if amount is negative (i.e., trying to use this method to increase the
        concentration of an element in the Cauldron).

        If the specified element is not present in the mix, the Cauldron is not changed.

        Arguments:
          element (str): element to be reduced/removed
          amount (float): concentration of the element to attempt to remove

        Returns:
          amount or current_amount (float): actual amount removed from the cauldron (0 if not present)
        """
        # TODO: validate the element, perhaps?
        assert amount >= 0, 'Distilling cannot increase the concentration of an element!'

        current_amount = self.elements.get(element, 0)

        if current_amount <= amount:
            return self.elements.pop(element, current_amount)
        else:
            self.elements[element] = self.elements[element] - amount
            return amount

    def brew(self):
        """Attempt to combine the elements in the cauldron into a matching potion.

        If a match is found, the cauldron's contents are cleared, otherwise just print a failure message

        Returns:
          result (Potion): a potion whose recipe matches the contents of the Cauldron, OR
          None: if the contents of the Cauldron don't match a potion in the list
        """
        results = alchemy.potion.get_matches(self.elements)
        if results:
            print("Success! The following concoctions can be brewed from the cauldron's contents:")
            for potion in results:
                print(' - ', potion.name)
            # TODO: narrow down the desired brew before clearing the cauldron
            #self.elements = {}
            return results[0]
        else:
            print('Oops, that\'s not a winning combination! Better try again...')
            return None
