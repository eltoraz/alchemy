"""Prototype for actually playing around with the alchemy system.

Mix ingredients in the cauldron to create potions, and store them in
your inventory. Drink (or otherwise apply) them, but most of the
effects won't actually do anything yet!
"""
from alchemy.cauldron import Cauldron

class Prototype:
    """The game (prototype) itself which provides a container for the
    involved components.
    """
    def __init__(self):
        self.main_cauldron = Cauldron()

    def run(self):
        """Setup the environment and run the main loop.
        """
        print("Alchemy game prototype",
              "By Bill Jameson (@eltoraz)", sep='\n', end='\n\n')

        print("Business has been slow in your potion shop today. You've left",
              "a sign on the counter and gone out back to brew up some more",
              "stock. Hey, it beats sitting around all day, right?", sep='\n')

        # main loop
        self.keep_going = True
        while self.keep_going:
            print("What do you want to do next?")
            command = input('> ')
            self.handle_input(command)

    def handle_input(self, command):
        # map available commands to methods that carry them out
        actions = {'quit': self.cmd_quit, 'exit': self.cmd_quit,
                   'help': self.cmd_help, 'check': self.cmd_check,
                   'add': self.cmd_add, 'distill': self.cmd_distill,
                   'brew': self.cmd_brew, 'empty_cauldron': self.cmd_empty}

        components = command.split(' ')
        verb = components[0].lower()

        actions.get(verb, self.cmd_unknown)(verb)

    def cmd_unknown(self, cmd, **kwargs):
        print("You briefly consider", cmd, "but decide against it.")
        print("(Unrecognized command; try 'help' for the accepted ones!)")

    def cmd_help(self, cmd, **kwargs):
        print("Actions available to you today:")
        print(" - help: show this message")
        print(" - quit (or exit): quit the game")
        print(" - check <object>: list information about specified category",
              "   - cauldron: elements in the cauldron",
              "   - reagents: ingredients you have in stock",
              "   - potions: potions you've already crafted", sep='\n')
        print(" - add <reagents>: add the reagents (separated by spaces) to"
              "     the cauldron", sep='\n')
        print(" - distill <element> <quantity>: remove an amount of the given",
              "     element from the caulrdon", sep='\n')
        print(" - brew: attempt to process the ingredients in the cauldron",
              "     into a potion", sep='\n')
        print(" - empty_cauldron - reset the caulrdon (irreversibly!)")

    def cmd_quit(self, cmd, **kwargs):
        print("That's enough of that. Back to the tedium of your empty shop!")
        self.keep_going = False

    def cmd_check(self, cmd, **kwargs):
        self.placeholder()

    def cmd_add(self, cmd, **kwargs):
        self.placeholder()

    def cmd_distill(self, cmd, **kwargs):
        self.placeholder()

    def cmd_brew(self, cmd, **kwargs):
        self.placeholder()

    def cmd_empty(self, cmd, **kwargs):
        self.placeholder()

    def placeholder(self):
        print("PLACEHOLDER TEXT")
