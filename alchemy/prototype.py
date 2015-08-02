"""Prototype for actually playing around with the alchemy system.

Mix ingredients in the cauldron to create potions, and store them in
your inventory. Drink (or otherwise apply) them, but most of the
effects won't actually do anything yet!
"""
from alchemy.cauldron import Cauldron
from alchemy.reagent import reagents

class Prototype:
    """The game (prototype) itself which provides a container for the
    involved components.
    """
    def __init__(self):
        self.main_cauldron = Cauldron()
        self.potions_brewed = []

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
            command = ''
            while command.strip() == '':
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

        actions.get(verb, self.cmd_unknown)(verb, components[1:])

    def cmd_unknown(self, cmd, *args):
        print("You briefly consider", cmd, "but decide against it.")
        print("(Unrecognized command; try 'help' for the accepted ones!)")

    def cmd_help(self, cmd, *args):
        print("Actions available to you today:")
        print(" - help: show this message")
        print(" - quit (or exit): quit the game")
        print(" - check <object>: list information about specified category",
              "   - cauldron: elements in the cauldron",
              "   - reagents: ingredients you have in stock",
              "   - potions: potions you've already crafted", sep='\n')
        print(" - add <reagents>: add the reagents (separated by spaces) to",
              "     the cauldron", sep='\n')
        print(" - distill <element> <quantity>: remove an amount of the given",
              "     element from the caulrdon", sep='\n')
        print(" - brew: attempt to process the ingredients in the cauldron",
              "     into a potion", sep='\n')
        print(" - empty_cauldron - reset the caulrdon (irreversibly!)")

    def cmd_quit(self, cmd, *args):
        print("That's enough of that. Back to the tedium of your empty shop!")
        self.keep_going = False

    def cmd_check(self, cmd, *args):
        if len(args[0]) == 0:
            # high-level overview
            print("You have", len(reagents), "types of reagents to work with.")
            if len(self.potions_brewed) == 1:
                print("You've brewed 1 potion today.")
            else:
                print("You've brewed", len(self.potions_brewed),
                      "potions today.")
            if self.main_cauldron.elements:
                print("You have a brew in progress.")
            else:
                print("The cauldron is empty.")
        else:
            category = args[0][0].lower()
            reagent_options = ['reagents', 'ingredients']
            potion_options = ['potions', 'stock', 'brews']
            if category == 'cauldron':
                # cauldron status
                if self.main_cauldron.elements:
                    print("You have a brew in progress containing:")
                    for element in self.main_cauldron.elements:
                        print(" -", self.main_cauldron.elements[element],
                              "units of", element)
                else:
                    print("The cauldron is empty.")
            elif category in reagent_options:
                # list of available reagents
                # TODO: limit line length for reagent list
                print("You have", len(reagents), "types of reagents to",
                      "work with:")
                print(" - ", end='')
                for reagent in reagents[:-1]:
                    print(reagent.name, end=', ')
                print(reagents[-1].name)
            elif category in potion_options:
                # list of potions crafted
                if len(self.potions_brewed) == 0:
                    print("0 potions brewed")
                elif len(self.potions_brewed) == 1:
                    print("1 potion brewed:")
                    print(" -", self.potions_brewed[0].name)
                else:
                    print(len(self.potions_brewed), "potions brewed:")
                    for i, potion in enumerate(self.potions_brewed):
                        print(" ", i+1, ". ", potion.name, sep='')
            else:
                # unknown argument
                self.cmd_unknown(' '.join(['checking'] + args[0]))

    def cmd_add(self, cmd, *args):
        self.placeholder()

    def cmd_distill(self, cmd, *args):
        self.placeholder()

    def cmd_brew(self, cmd, *args):
        self.placeholder()

    def cmd_empty(self, cmd, *args):
        self.placeholder()

    def placeholder(self):
        print("PLACEHOLDER TEXT")
