"""An actor in the game world - NPCs, monsters, and the player
themself.
"""
class Character:
    """A character

    Arguments:
      name (str): the actor's display name
      max_hp (int): represents the amount of damage the actor can take
                    before falling unconscious/dying

    Attributes:
    """
    # TODO: check that stat values are reasonable
    def __init__(self, name='', hp=1):
        # basic properties
        self.name = name
        self.max_hp = hp
        self.current_hp = hp

        # status
        self.effects = {}

    # TODO: eventually move away from just strings to reperesent/
    #       identify efffects?
    # TODO: process effect start triggers (once implemented)
    def apply_status(self, effect, duration):
        """Apply the specified effect to the actor, applying any
        associated triggers (stat buffs, speed modifiers, etc.)

        If the effect is already present, extend the duration. Or if
        it's a permanent status just set the duration to -1.

        Passing a duration of 0 or less (apart from -1, which
        signifies a permanent effect), or trying to apply a status
        that already exists on a permanent basis, fails.

        Arguments:
          effect (str): the effect to add
          duration (number): duration of the status effect in ticks

        Returns:
          duration of the effect in ticks (if the effect was already
            present, this will be the extended time), OR
          None, if no change was made
        """
        # no change if the specified effect is already present but
        # permanent, or if the duration passed makes no sense
        if (duration != -1 and duration <= 0 or 
                self.effects.get(effect, 0) == -1):
            return None

        result = duration
        if effect in self.effects and duration != -1:
            result += self.effects[effect]
        self.effects[effect] = result

        return result

    # TODO: process effect ending triggers (once implemented)
    def dispell(self, effect):
        """Remove the specified effect from the actor, processing all
        its ending triggers.

        Arguments:
          effect (str): the effect to remove

        Returns:
          time left on the effect's timer (-1 if a permament) OR
          None if the effect wasn't present on the actor
        """
        return self.effects.pop(effect, None)

    def tick(self, speed=1):
        """Progress timer-based properties for the actor by one step.

        Arguments:
          speed (number): number of ticks to progress timers
        """
        keys = [key for key in self.effects]
        for effect in keys:
            # TODO: apply any, er, effects of the status condition
            #       (poison damage, etc.)

            if self.effects[effect] != -1:
                # -1 represents a permanent effect, so don't change
                # the counter
                self.effects[effect] -= speed

                if self.effects[effect] <= 0:
                    # remove effect when it expires
                    self.dispell(effect)
