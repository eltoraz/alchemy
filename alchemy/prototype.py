"""Prototype for actually playing around with the alchemy system.

Mix ingredients in the cauldron to create potions, and store them in
your inventory. Drink (or otherwise apply) them, but most of the
effects won't actually do anything yet!
"""
from alchemy.cauldron import Cauldron
from alchemy.reagent import get_reagents, reagents

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
        """Delegate handling of commands to helper functions.

        Arguments:
          command (str): (space-separated) verb followed by optional
                         arguments that define the player's actions
        """
        # map available commands to methods that carry them out
        actions = {'quit': self.cmd_quit, 'exit': self.cmd_quit,
                   'help': self.cmd_help, 'check': self.cmd_check,
                   'add': self.cmd_add, 'distill': self.cmd_distill,
                   'brew': self.cmd_brew, 'empty_cauldron': self.cmd_empty}

        components = command.split(' ')
        verb = components[0].lower()

        actions.get(verb, self.cmd_unknown)(verb, *components[1:])

    def cmd_unknown(self, cmd, *args, **kwargs):
        """Fallback for unrecognized commands. Suggest that the player
        ask for help if their command failed.

        Arguments:
          cmd (str): command (that failed in this case)
          args: unused, but present here for consistency
          kwargs: 'msg' can be defined to display a custom error
        """
        if 'msg' in kwargs:
            print(kwargs['msg'])
        else:
            print("You briefly consider", cmd, "but decide against it.")
        print("(Unrecognized command; try 'help' for the accepted ones!)")

    def cmd_help(self, cmd, *args):
        """Print a brief overview of available commands.

        Arguments: cmd (the command) required for consistency with the
        other helper functions, but not used. args: unused as well.
        """
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
        """Set the flag used by the main loop to false to gracefully
        exit the game.

        Arguments: cmd (the command) required for consistency with the
        other helper functions, but not used. args: unused as well
        """
        print("That's enough of that. Back to the tedium of your empty shop!")
        self.keep_going = False

    def cmd_check(self, cmd, *args):
        """Check the status of the specified object, or if none
        specified, give a high-level overview of the game state.

        Arguments:
          cmd (str): the command used (not used here but required for
                     consistency with the other helper functions)
          args: the main loop passes the other arguments as a list of
                str into args; if empty this triggers the high-
                level overview, but if it's a recognized category a
                context-sensitive description is provided
        """
        if len(args) == 0:
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
            category = args[0].lower()
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
                self.cmd_unknown(' '.join(['checking'] + args))

    def cmd_add(self, cmd, *args):
        """Add the named ingredient to the cauldron.

        If the reagent does not match any in the list, display an
        error and don't change the cauldron.

        Arguments:
          cmd (str): the command (required for consistency with the
                     other helper functions but not used)
          args: the main loop passes the other arguments as a list of
                str into args; this list must have the name of
                exactly one reagent to add
        """
        error = ""
        if len(args) == 0:
            error = "You want to add something to the cauldron, but you\n" + \
                    "don't know exactly what yet."
        elif len(args) > 1:
            # for now, can only add 1 ingredient at a time
            # TODO: recursively add multiple ingredients, BUT need to
            #       do error checking before adding any
            error = "You consider a few reagents to add, but decide to\n" + \
                    "add them one at a time. These things can be delicate!"
        else:
            target_reagent = get_reagents(args[0])
            # TODO: catch cases where multiple results are returned,
            #       whenever I change the search algorithm
            if len(target_reagent) == 0:
                error = "After rooting around for " + args[0] + " you\n" + \
                        "reluctantly determine that you don't have any\n" + \
                        "to add to your brew."
            else:
                self.main_cauldron.add_ingredients(target_reagent[0])
                print("You add", args[0], "to the cauldron, being sure to")
                print("observe all precautions while handling it.")

        if error:
            self.cmd_unknown(cmd, *args, msg=error)

    def cmd_distill(self, cmd, *args):
        self.placeholder()

    def cmd_brew(self, cmd, *args):
        self.placeholder()

    def cmd_empty(self, cmd, *args):
        self.placeholder()

    def placeholder(self):
        print("|PLACEHOLDER TEXT|")
