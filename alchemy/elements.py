'''
Types of magic from PK's floraverse
Ref:
  - http://floraverse.deviantart.com/journal/Elements-guide-425648924
  - https://docs.google.com/spreadsheets/d/1yoH7I7zblp1gfJztv24-HiPUY-MqXuGxUIznfKqvOng/edit#gid=0
'''
# this is mostly used to index the element table (the empty string key allows us to get
# primary as well as secondary elements)
primary_elements = {'': 0,
                    'Fire': 1,
                    'Water': 2,
                    'Air': 3,
                    'Earth': 4,
                    'Spirit': 5}

element_table = [['',       'Fire',   'Water',    'Air',      'Earth',    'Spirit'],
                 ['Fire',   'Plasma', 'Acid',     'Light',    'Lava',     'Aura'],
                 ['Water',  'Acid',   'Ice',      'Cloud',    'Clay',     'Poison'],
                 ['Air',    'Light',  'Cloud',    'Storm',    'Sand',     'Sound'],
                 ['Earth',  'Lava',   'Clay',     'Sand',     'Crystal',  'Magnet'],
                 ['Spirit', 'Aura',   'Poison',   'Sound',    'Magnet',   'Psi']]

def get_element(first, second=''):
    # TODO: perhaps use a more useful representation of the elements than a string
    return element_table[primary_elements[first]][primary_elements[second]]

