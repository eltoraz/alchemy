'''
Tests for the cauldron
'''
from nose.tools import eq_

from alchemy.reagent import Reagent
from alchemy.potion import Potion
from alchemy.cauldron import Cauldron

test_water = Reagent('testwater', 'water reagent for testing', [{'element': 'Water', 'concentration': 11.0}])
test_spirit = Reagent('testspirit', 'spirit reagent for testing', [{'element': 'Spirit', 'concentration': 0.5}])
test_healpot = Potion('testheal', 'healing potion for testing',
                        [{'effect': 'restore_health', 'magnitude': 25.0}],
                        [{'element': 'Water', 'min': 10.0, 'max': 12.0}, {'element': 'Spirit', 'min': 0.1, 'max': 1.0}])

def test_create_empty():
    test_cauldron = Cauldron([])
    eq_(test_cauldron.elements, {})

def test_create():
    test_cauldron = Cauldron([test_water, test_spirit])
    eq_(test_cauldron.elements, {'Water': 11.0, 'Spirit': 0.5})

# TODO: tests for adding a reagent, distilling, brewing
