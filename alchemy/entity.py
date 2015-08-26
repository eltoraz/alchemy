"""An actor in the game world - NPCs, monsters, and the player
themself.
"""
class Entity:
    """An entity

    Arguments:
      name (str): the actor's display name
      max_hp (int): represents the amount of damage the actor can take
                    before falling unconscious/dying

    Attributes:
    """
    def __init__(self, name='', max_hp=1):
        # basic properties
        self.name = name
        self.max_hp = max_hp

        # status
        self.effects = {}

    # TODO: process effect ending triggers (once implemented)
    # TODO: eventually move away from just strings to reperesent/
    #       identify efffects?
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
        for effect in self.effects:
            # TODO: apply any, er, effects of the status condition
            #       (poison damage, etc.)

            if self.effects[effect] != -1:
                # -1 represents a permanent effect, so don't change
                # the counter
                self.effects[effect] -= speed

                if self.effects[effect] <= 0:
                    # remove effect when it expires
                    self.dispell(effect)
