"""Character tests
"""
from nose.tools import eq_

from alchemy.character import Character

def test_create():
    null_actor = Character()
    eq_(null_actor.name, '')
    eq_(null_actor.max_hp, 1)
    eq_(null_actor.current_hp, 1)

    player = Character('you', 10)
    eq_(player.name, 'you')
    eq_(player.max_hp, 10)
    eq_(player.current_hp, 10)

def test_apply_status():
    char = Character()
    result = char.apply_status('poison', 1)
    eq_(result, 1)
    eq_(len(char.effects), 1)
    eq_(char.effects['poison'], 1)

    # add a second status
    result = char.apply_status('haste', 3)
    eq_(result, 3)
    eq_(len(char.effects), 2)
    eq_(char.effects['haste'], 3)

    # extend the first status effect's duration
    result = char.apply_status('poison', 4)
    eq_(result, 5)
    eq_(len(char.effects), 2)
    eq_(char.effects['poison'], 5)

    # try some invalid durations
    result = char.apply_status('poison', 0)
    eq_(result, None)
    eq_(char.effects['poison'], 5)

    result = char.apply_status('poison', -2)
    eq_(result, None)
    eq_(char.effects['poison'], 5)

    # permanent status effects
    result = char.apply_status('existential dread', -1)
    eq_(result, -1)
    eq_(len(char.effects), 3)
    eq_(char.effects['existential dread'], -1)

    # change a temporary status to a permanent one
    result = char.apply_status('haste', -1)
    eq_(result, -1)
    eq_(len(char.effects), 3)
    eq_(char.effects['haste'], -1)

def test_dispell():
    char = Character()
    char.apply_status('poison', 3)
    char.apply_status('haste', 3)
    eq_(len(char.effects), 2)

    result = char.dispell('poison')
    eq_(result, 3)
    eq_(len(char.effects), 1)
    eq_(char.effects.get('poison', None), None)

    # try dispelling the status again
    result = char.dispell('poison')
    eq_(result, None)
    eq_(len(char.effects), 1)
    eq_(char.effects.get('poison', None), None)

    # dispell a status that was never present
    result = char.dispell('burning')
    eq_(result, None)
    eq_(len(char.effects), 1)
    eq_(char.effects.get('burning', None), None)

def test_tick():
    char = Character()
    char.apply_status('poison', 1)
    char.apply_status('haste', 3)
    char.apply_status('existential dread', -1)
    eq_(len(char.effects), 3)

    # one tick, which expires 'poison'
    char.tick()
    eq_(len(char.effects), 2)
    eq_(char.effects.get('poison', None), None)
    eq_(char.effects['haste'], 2)
    eq_(char.effects['existential dread'], -1)

    # 2 ticks
    char.tick()
    eq_(len(char.effects), 2)
    eq_(char.effects['haste'], 1)
    eq_(char.effects['existential dread'], -1)

    # 3 ticks, which expires 'haste'
    char.tick()
    eq_(len(char.effects), 1)
    eq_(char.effects.get('haste', None), None)
    eq_(char.effects['existential dread'], -1)

    # 4 ticks, which should have no additional impact effect-wise
    char.tick()
    eq_(len(char.effects), 1)
    eq_(char.effects['existential dread'], -1)

    # TODO: test ticking with different speeds
