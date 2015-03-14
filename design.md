You've found what passes for a design doc for this little alchemy project!
But for now it's mostly just a braindump of things I'm working on/figuring out now.
I have an even sketchier document going of random ideas to possibly work into this world later, but I'd
really like to keep the scope of this pretty narrow for now.

### Inspirations

- Open world, abundance of reagents in *The Elder Scrolls*, particularly *Oblivion* and *Skyrim*
- Exploring the universe in *Starbound*, collecting seeds, and building a farm of alien and more mundane crops
- The approach to magic outlined in [this page of the flora comic](http://floraverse.com/comic/flora/page/208-basic-guide-to-magic/)

### The gist of it

Mixing/cooking/processing reagents together yields a potion dependent on:
- combined concentrations of elements in ingredients
- special properties possessed by rare/otherwise important ingredients
- ambient/environmental factors (magical artifacts, affinity of player/NPC assistants in close proximity)

### Basic implementation

When trying to define the potions themselves, I came up with two potential approaches.
It really comes down to how a potion is defined. Is it generic container to hold effects?
Or is each one an entity that contains its own specific effects? Writing the options out this way doesn't
really do much for the divide between the different implementations.

Using the generic container approach, crafting a potion would come down to mixing ingredients to give you the effects
you want. There wouldn't be a "healing potion" per se - you'd pick ingredients with the right elements to produce
the "restore_health" effect. In essence, each individual **effect** would have its own recipe dictating which elements
and in what proportions you'd need to mix to get it. I'm kind of averse to this approach, partly because it's basically the 
[alchemy process from the *Elder Scrolls* series](http://uesp.net/wiki/Skyrim:Alchemy) with an additional layer of
complexity between the player and the crafting process (namely, the elements). While TES alchemy is an inspiration for
this project, another part of it was wanting to be different to fix some of the complaints I had - especially how the
various potions you could craft, while useful, didn't really feel unique and special.

A large pool of interesting effects is part of the solution to this problem, and another will having the actual alchemy
process be more engaging than "select ingredients, then click combine." These points are making me lean towards the
other option - define potions individually, with a list of effects and a "recipe" of the required elements (and their
proportions). It's more rigid in that you won't have the freedom to mix whatever effects you want, but it will hopefully
be easier to balance this way. I want to dodge some of the problems in *Starbound's* cooking system - it has a nice
large variety of dishes to prepare, but lots of them are hidden behind an obtuse "tech tree"-like progression, and they
don't actually give you any metrics on what anything actually **does**.

All in all, these are just early thoughts - adding in "special" reagents with unique properties should open up the
potion design space too. But I'm glad I wrote that out, since it helped me decide how to proceed for now.

### Elemental interaction

A couple ways to handle mixing elements from reagents:
- combine them to form the given secondary/tertiary element with a concentration relative to the constituents
- have the resultant concoction retain the elements of the reagents (perhaps with a slight loss from processing)

The second could possibly incorporate the first via a separate mechanism - a process to promote elements combining.
Which would be less complex overall? The first has more to keep in mind from the start (elemental combinatorics).
The second has more moving parts but seems like a shallower learning curve to introduce.

### Potion types and effects

Not limited to drinkable concoctions!
Including but not limited to potions, salves, poisons, volatile mixtures (explosive/corrosive/otherwise damaging on contact).
The important thing is having a wide variety of mundane and more interesting effects since this is a core gameplay element.

- healing (raw health recovery and regen)
- generic antidotes for various poisons, as well as specialized antidotes for rarer/more virulent ones
- general panacea for common but weak ailments
- resist X element
- resist X environmental factor (e.g., extreme heat but not necessarily Fire)
- boost abilities of X element
- temporary boost to specific physical abilities
- temporary boost to specialized skills
- "vanilla"/physical poison
- "magical" poison (specifically target foes' elemental weakness)
- supress magical abilities
- illumination
- sense/perception enhancers (night vision, sense magic, etc.)
- "pheromone" concoctions - use to alter behavior of other creatures
- explosives (e.g., detonates on contact with a specific substance/elemental influence)
- corrosive mixtures (traditional acid, but also specialized ones that act on targeted substances or magic types)
- waterbreathing
- berserk
- stun
- slow
- haste
- perhaps not a true invisibility but a chameleon-like camouflage effect
- concentration of X element

