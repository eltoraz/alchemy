"""Text adventure prototype to start playing around with the alchemy
framework.

Mix ingredients in the cauldron to create potions, and store them in
your inventory. Drink (or otherwise apply) them, but most of the
effects won't actually do anything yet!
"""
from alchemy.cauldron import Cauldron
from alchemy.character import Character
from alchemy.elements import element_set
from alchemy.reagent import get_reagents, reagents

class Game:
    """The game itself which provides a container for the involved
    components.
    """
    def __init__(self):
        self.main_cauldron = Cauldron()
        self.potions_brewed = []

        self.player = Character('you', 15)

    def run(self):
        """Setup the environment and run the main loop.
        """
        print("Alchemy game text adventure prototype",
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

            self.player.tick()

    # TODO: use pprint module instead of manually formatting strings
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

        actions.get(verb, self.cmd_error)(verb, *components[1:])

    # TODO: perform text formatting here so msg being passed in doesn't
    #       need to be manually line-broken by the caller
    def cmd_error(self, cmd, *args, **kwargs):
        """Fallback for unrecognized commands. Suggest that the player
        ask for help if their command failed.

        Arguments:
          cmd (str): command (that failed in this case)
          args: unused, but present here for consistency
          kwargs: 'msg' can be defined to display a custom error
        """
        if 'msg' in kwargs:
            print(kwargs['msg'])
            print("(There was an error in your command; watch out for typos",
                  "or try 'help' for notes on accepted syntax)", sep='\n')
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
              "   - self: player status",
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

    # TODO: check elements for reference?
    def cmd_check(self, cmd, *args):
        """Check the status of the specified object, or if none
        specified, give a high-level overview of the game state.

        Arguments:
          cmd (str): the command used (not used here but required for
                     consistency with the other helper functions)
          args: the main loop passes the other user-entered parameters
                as positional arguments; if empty this triggers the
                high-level overview, but if it's a recognized category
                a context-sensitive description is provided
        """
        if len(args) == 0:
            # high-level overview
            print("You have ", self.player.current_hp, "/", self.player.max_hp,
                  " hp left and have ", len(self.player.effects),
                  sep='', end='')
            if len(self.player.effects) == 1:
                print(" status condition.")
            else:
                print(" status conditions.")
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
            self_options = ['self', 'player', 'me']
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
            elif category in self_options:
                # player status
                print("You have ", self.player.current_hp, "/",
                      self.player.max_hp, " hp left.", sep='')
                if len(self.player.effects) == 0:
                    print("You have no unusual status conditions.")
                else:
                    print("You are currently under the influence of the",
                          "following status conditions:")
                    player_effects = self.player.effects
                    # TODO: needs to be updated if effects changes to
                    #       use something other than string as the key
                    for effect in player_effects:
                        print(" - ", effect, ": ", player_effects[effect],
                              " rounds", sep='')
            else:
                # unknown argument(s)
                self.cmd_error(' '.join(['checking'] + list(args)))

    def cmd_add(self, cmd, *args):
        """Add the named ingredient to the cauldron.

        If the reagent does not match any in the list, display an
        error and don't change the cauldron.

        Arguments:
          cmd (str): the command (required for consistency with the
                     other helper functions but not used)
          args: the main loop passes the other user-entered parameters
                as positional arguments; exactly one is required
                args[0] must be the name of a reagent to add
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
            self.cmd_error(cmd, *args, msg=error)

    def cmd_distill(self, cmd, *args):
        """Distill the contents of the caulrdon, removing a specified
        amount of a specified element.

        If the element specified is invalid or not present in the
        cauldron, display an error and make no changes.

        Arguments:
          cmd (str): this command (required for consistency with other
                     helper functions but otherwised not used here)
          args: the main loop passes the other user-entered parameters
                as positional arguments; 1 is required, 1 is optional
                args[0] must be the element to remove
                args[1] is the quantity to remove (all present if
                        omitted)
        """
        element = ''
        error = ""
        amount = 0.0

        if not self.main_cauldron.elements:
            error = "It's going to be awfully hard to distill something\n" + \
                    "from an empty cauldron!"
        elif len(args) == 0:
            error = "You can siphon off any single element from the\n" + \
                    "cauldron, but you need to decide which one!"
        elif len(args) > 2:
            error = "Distillation can be a delicate process; you should\n" + \
                    "concentrate on it without distractions! (Too many\n" + \
                    "arguments specified - max 2, the element and amount)"
        else:
            element = args[0].capitalize()
            if element not in element_set:
                error = "You're not quite sure why it crossed your mind\n" + \
                        "try to distill " + element + ", but you rightly\n" + \
                        "realize that it's not an element."
            elif len(args) == 1:
                amount = self.main_cauldron.elements.get(element, 0.0)
            else:
                try:
                    amount = float(args[1])
                except ValueError:
                    error = "You prepare to distill " + element + " but\n" + \
                            "quickly realize you've miscalibrated your\n" + \
                            "measuring apparatus! (Amount to distill not\n" + \
                            "recognized as a number)"

        if not error:
            try:
                actual_amount = self.main_cauldron.distill(element, amount)
            except AssertionError as e:
                error = '\n'.join([e.args[0],
                                  "And you thought you were onto something."])
            else:
                if actual_amount > 0.0:
                    print("You carefully distill", actual_amount, "units of",
                        element, "from the mixture.")
                else:
                    print("You try to distill", element, "from the mixture in",
                          "the cauldron, but quickly come to the conclusion",
                          "that it wasn't present in the first place!")

        if error:
            self.cmd_error(cmd, *args, msg=error)

    def cmd_brew(self, cmd, *args):
        """Brew the contents of the cauldron into a potion.

        If the elements in the cauldron are a superset of those in a
        recipe, and the proportions are within the specified limits,
        add the potion to the list and empty the cauldron.

        Currently, extra elements present will not affect success here
        unless they comprise another recipe.

        Arguments:
          cmd (str): this command (required for consistency with other
                     helper functions but otherwise not used here)
          args: the main loop passes the other user-entered parameters
                as positional arguments, but they're not used/checked
        """
        if not self.main_cauldron.elements:
            print("If you could brew potions from nothing you'd be rich! But",
                  "that skill eludes you for now.", sep='\n')
            return

        result_count = len(self.main_cauldron.possible_results)
        if result_count == 0:
            print("The contents of the cauldron aren't reacting to form a",
                  "complete potion yet. Keep at it!", sep='\n')
        elif result_count > 1:
            print("The mix is reacting! Judging from the appearance and odor",
                  "wafting from it, the following brews could be created with",
                  "just a little more effort:", sep='\n')
            for potion in self.main_cauldron.possible_results:
                print(" -", potion.name)
        else:
            elements_used = self.main_cauldron.elements
            elements_list = list(elements_used)
            result = self.main_cauldron.brew()
            if result:
                self.potions_brewed.append(result)
                print("Brew successful! Created", result.name, "from ", end='')
                for element in elements_list[:-1]:
                    print(elements_used[element], " units of ", element, ", ",
                          sep='', end='')
                print("and ", elements_used[elements_list[-1]], " units of ",
                      elements_list[-1], ".", sep='')
            else:
                print("The brew is nearly complete! Some of the element\n"
                      "concentrations are too high to make a ",
                      self.main_cauldron.possible_results[0].name, sep='')
                for element in self.main_cauldron.possible_results[0].recipe:
                    if elements_used[element['element']] > element['max']:
                        print(" - ", element['element'], ": max ",
                              element['max'], ", but ",
                              elements_used[element['element']],
                              " units present", sep='')

    def cmd_empty(self, cmd, *args):
        """Remove all elements from the cauldron.

        If the cauldron is already empty, this wouldn't do anything
        anyway, but it's always nice to give the player a different
        bit of feedback.

        Arguments:
          cmd (str): this command (required for consistency with other
                     helper functions but otherwised not used here)
          args: the main loop passes the other user-entered parameters
                as positional arguments, but they're not used/checked
        """
        if not self.main_cauldron.elements:
            print("The cauldron is already empty. How convenient!")
        else:
            self.main_cauldron.empty()
            print("Dissatisified with the mixture you're working on, you",
                  "drain the cauldron and prepare to start over.", sep='\n')
