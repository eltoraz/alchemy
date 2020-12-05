"""Types of magic. Most things will have an elemental affinity that
governs behavior, interactions, etc.
"""
# this is mostly used to index the element table (the empty string key
# allows us to get primary as well as secondary elements)
primary_elements = {'Void': 0,
                    'Fire': 1,
                    'Water': 2,
                    'Air': 3,
                    'Earth': 4,
                    'Lightning': 5,
                    'Ice': 6,
                    'Light': 7,
                    'Shadow': 8,
                    'Acid': 9,
                    'Soul': 10}

# TODO: elemental combinatorics?
def get_element(first, second=''):
    """Return the element resulting from combining the specified
    primary elements.

    Specifying '' and a primary element yields a primary element, and
    calling the function with two primary elements will yield the
    corresponding secondary element from combining the two.

    Arguments:
      first (str): primary element
      second (str): primary element (default '')

    Returns:
      element (str): primary/secondary element
    """
    
    return first
