"""
Types of magic from PK's floraverse
"""
# For reference:
#   - http://floraverse.deviantart.com/journal/Elements-guide-425648924
#   - https://docs.google.com/spreadsheets/d/1yoH7I7zblp1gfJztv24-HiPUY-MqXuGxUIznfKqvOng/edit#gid=0

# this is mostly used to index the element table (the empty string key
# allows us to get primary as well as secondary elements)
primary_elements = {'': 0,
                    'Fire': 1,
                    'Water': 2,
                    'Air': 3,
                    'Earth': 4,
                    'Spirit': 5}

element_table = \
           [['',       'Fire',   'Water',    'Air',      'Earth',    'Spirit'],
            ['Fire',   'Plasma', 'Acid',     'Light',    'Lava',     'Aura'],
            ['Water',  'Acid',   'Ice',      'Cloud',    'Clay',     'Poison'],
            ['Air',    'Light',  'Cloud',    'Storm',    'Sand',     'Sound'],
            ['Earth',  'Lava',   'Clay',     'Sand',     'Crystal',  'Magnet'],
            ['Spirit', 'Aura',   'Poison',   'Sound',    'Magnet',   'Psi']]

def get_element(first, second=''):
    """Return the element resulting from combining the specified
    primary elements.

    Specifying '' and a primary element yields a primary element, and
    calling the function with two primary elements will yield the
    corresponding secondary element.

    Arguments:
      first (str): primary element
      second (str): primary element (default '')

    Returns:
      element (str): primary/secondary element
    """
    # TODO: perhaps use a more useful representation of the elements
    #       than a string
    # TODO: (far off): tertiary elements?!
    return element_table[primary_elements[first]][primary_elements[second]]

