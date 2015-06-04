'''
Tests for the cauldron
'''
from nose.tools import eq_, raises

from alchemy.reagent import Reagent
from alchemy.potion import Potion
from alchemy.cauldron import Cauldron

test_water = Reagent('testwater', 'water reagent for testing', [{'element': 'Water', 'concentration': 11.0}])
test_spirit = Reagent('testspirit', 'spirit reagent for testing', [{'element': 'Spirit', 'concentration': 0.5}])
test_healpot = Potion('healing potion', 'just your average vitality-restoring potion',
                      [{'effect': 'restore_health', 'magnitude': 25.0}],
                      [{'element': 'Water', 'min': 10.0, 'max': 12.0}, {'element': 'Spirit', 'min': 0.1, 'max': 1.0}])

def test_create():
    # Creating a cauldron with no ingredients has no elements
    empty_cauldron = Cauldron([])
    eq_(empty_cauldron.elements, {})

    test_cauldron = Cauldron([test_water, test_spirit])
    eq_(test_cauldron.elements, {'Water': 11.0, 'Spirit': 0.5})

def test_add_reagent():
    test_cauldron = Cauldron([])

    # note: add_ingredients() can take an arbitrary number of reagents
    test_cauldron.add_ingredients(Reagent('onthefly', 'n/a', [{'element': 'Air', 'concentration': 4.0}]))
    eq_(test_cauldron.elements, {'Air': 4.0})

    test_cauldron.add_ingredients(test_water, test_spirit)
    eq_(test_cauldron.elements, {'Air': 4.0, 'Water': 11.0, 'Spirit': 0.5})

    test_cauldron.add_ingredients(test_water)
    eq_(test_cauldron.elements['Water'], 22.0)

def test_distill():
    test_cauldron = Cauldron([test_water, test_spirit])

    # distill() can reduce the amount of a given element or remove it entirely
    # it raises an AssertionError if trying to increase an element
    # it returns the amount removed (0 if not present, hence none removed)
    result = test_cauldron.distill('Water', 4.0)
    eq_(result, 4.0)
    eq_(test_cauldron.elements, {'Water': 7.0, 'Spirit': 0.5})

    result = test_cauldron.distill('Water', 7.0)
    eq_(result, 7.0)
    eq_(test_cauldron.elements, {'Spirit': 0.5})

    result = test_cauldron.distill('Water', 1.0)
    eq_(result, 0)
    eq_(test_cauldron.elements, {'Spirit': 0.5})
    
@raises(AssertionError)
def test_distill_increase_element():
    test_cauldron = Cauldron([test_spirit])
    test_cauldron.distill('Water', -11.0)

def test_brew():
    # matches a recipe
    test_cauldron = Cauldron([test_water, test_spirit])
    result = test_cauldron.brew()
    eq_(result.name, test_healpot.name)
    eq_(result.description, test_healpot.description)
    eq_(result.effects, test_healpot.effects)
    eq_(result.recipe, test_healpot.recipe)
    eq_(test_cauldron.elements, {})

    # matches elements but not quantities
    test_cauldron.add_ingredients(test_water, test_spirit,
                                  Reagent('toomuch', 'morespirit', [{'element': 'Spirit', 'concentration': 0.6}]))
    result = test_cauldron.brew()
    eq_(result, None)
    eq_(test_cauldron.elements, {'Water': 11.0, 'Spirit': 1.1})

    # no match
    test_cauldron.add_ingredients(Reagent('onthefly', 'n/a', [{'element': 'Air', 'concentration': 4.0}]))
    result = test_cauldron.brew()
    eq_(result, None)
    eq_(test_cauldron.elements, {'Water': 11.0, 'Spirit': 1.1, 'Air': 4.0})
