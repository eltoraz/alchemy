'''
Tests for reagents
'''
from nose.tools import eq_

from alchemy.reagent import Reagent

def test_create():
    test_elements = [{'element': 'Aura', 'concentration': 5.0},
                     {'element': 'Earth', 'concentration': 8.0}]
    ingredient = Reagent('chocolate', 'food of the gods', test_elements)
    eq_(ingredient.name, 'chocolate')
    eq_(ingredient.description, 'food of the gods')
    eq_(ingredient.elements, test_elements)

# TODO: test __repr__/__str__?
