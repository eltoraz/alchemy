"""
Miscellaneous shared utility functions
"""
from ast import literal_eval

# XML attributes always parse as strings with the standard etree XML library,
# so convert known numbers present to the correct type
# Currently supports: reagent.elements, potion.effect, potion.recipe
# TODO: catch ValueError raised if the XML attrib is malformed/invalid
def eval_xml_numbers(orig_dict):
    """Parse numbers from certain strings obtained from reading in an XML file

    Arguments:
      orig_dict (dict): dict with some numeric values, currently represented as str

    Returns:
      result (dict): original dict with numeric values converted from str -> float
    """
    result = orig_dict
    number_attribs = ['magnitude', 'duration', 'min', 'max', 'concentration']

    for key in orig_dict:
        if key in number_attribs:
            result[key] = literal_eval(orig_dict[key])

    return result
