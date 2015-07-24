'''
Tests for potions
'''
from nose.tools import eq_

import alchemy.potion
from alchemy.potion import PotionType, Potion

def test_create():
   name = 'test healer'
   desc = 'WAY TOO STRONG'
   cat = PotionType['potion']
   eff  = [{'effect': 'restore_health', 'magnitude': 250.0}, {'effect': 'regen', 'magnitude': 10.0}]
   rec  = [{'element': 'Clay', 'min': 1.0, 'max': 5.0}, {'element': 'Aura', 'min': 1.0, 'max': 5.0}]
   test_potion = Potion(name, cat, desc, eff, rec)

   eq_(test_potion.name, name)
   eq_(test_potion.main_type, cat)
   eq_(test_potion.subtype, None)
   eq_(test_potion.description, desc)
   eq_(test_potion.effects, eff)
   eq_(test_potion.recipe, rec)

# some overlap with brew in cauldron tests
# TODO: rewrite this test so it doesn't need to be rewritten every time the relevant potion from
#       the potions list gets tweaked
def test_get_matches():
    test_elements = {'Fire': 5.0, 'Storm': 6.0}
    results_set = alchemy.potion.get_matches(test_elements)
    eq_(len(results_set), 1)
    result = results_set[0]
    eq_(result.name, 'haste salve')
    eq_(result.main_type, PotionType['salve'])
    eq_(result.subtype, None)
    eq_(result.description, "Apply to your ankles (or your species' equivalent)")
    eq_(result.effects, [{'effect': 'haste', 'magnitude': 2.0}])
    eq_(result.recipe, [{'element': 'Fire', 'min': 5.0, 'max': 10.0},
                        {'element': 'Storm', 'min': 6.0, 'max': 8.0}])

    multiple_matches = {'Fire': 8.0, 'Storm': 6.0, 'Air': 2.0}
    results_set = alchemy.potion.get_matches(multiple_matches)
    eq_(len(results_set), 2)
    eq_(results_set[0].name, 'haste salve')
    eq_(results_set[1].name, 'weak explosive')

    concentration_mismatch = {'Fire': 11.0, 'Storm': 2.0}
    result = alchemy.potion.get_matches(concentration_mismatch)
    eq_(result, [])

    non_matching_elements = {'Acid': 50.0, 'Lava': 100.0, 'Psi': 40.0}
    result = alchemy.potion.get_matches(non_matching_elements)
    eq_(result, [])
