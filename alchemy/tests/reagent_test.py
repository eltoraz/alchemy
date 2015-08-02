'''
Tests for reagents
'''
from nose.tools import eq_

import alchemy.reagent
from alchemy.reagent import Reagent

def test_create():
    test_elements = [{'element': 'Aura', 'concentration': 5.0},
                     {'element': 'Earth', 'concentration': 8.0}]
    ingredient = Reagent('chocolate', 'food of the gods', test_elements)
    eq_(ingredient.name, 'chocolate')
    eq_(ingredient.description, 'food of the gods')
    eq_(ingredient.elements, test_elements)

def test_get_reagents():
    null_result = alchemy.reagent.get_reagents('NOMATCH')
    eq_(null_result, [])

    one_result = alchemy.reagent.get_reagents('sugar')
    eq_(len(one_result), 1)
    eq_(one_result[0].name, 'sugar')

# TODO: test __repr__/__str__?
