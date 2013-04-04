#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set sts=4 sw=4 et :
#
# Authors:
#  Nirbheek Chauhan <nirbheek.chauhan@gmail.com>
# License:
#  AGPL-3.0
#  http://www.gnu.org/licenses/agpl-3.0.html
#
# Converts Unicode Devanagari text to Bharati Braille
#

import re
import sys

if sys.version_info.major != 3:
    raise Exception("This program needs Python 3!")

from mappings import virama
from mappings import akhand
from mappings import punctuation, vowels, consonants, various_signs
# We don't convert numbers and mathematical symbols yet
#from mappings import numbers, math_symbols

# Characters that need to be converted in the first pass
priority_mappings = akhand
# Aggregate characters that are directly subsituted for their braille equivalents
simple_mappings = {}
for each in punctuation, vowels, consonants, various_signs:
    simple_mappings.update(each)

# Reverse the braille-to-devanagari mapping.
# We need a devanagari-to-braille mapping
d_to_b = {}
for (braille, devanagari_list) in simple_mappings.items():
    for each in devanagari_list:
        d_to_b[each] = braille

# Reverse the braille-to-devanagari mapping.
# We need a devanagari-to-braille mapping
d_to_b_priority = {}
for (braille, devanagari_list) in priority_mappings.items():
    for each in devanagari_list:
        d_to_b_priority[each] = braille

def convert_devanagari_to_braille(text, debug=False):
    """
    Converts the given text from Devanagari to Bharati Braille
    Leaves unknown characters untouched
    """
    new_text = text
    # Do a string substitution for the string-to-char conversion
    for (key, value) in d_to_b_priority.items():
        new_text = new_text.replace(key, value)
    if debug:
        print ("After string-to-char conversion:\n"+new_text)
    # Create a translation table for unicode characters
    # This is faster than a string replacement
    new_text = new_text.translate(str.maketrans(d_to_b))
    if debug:
        print ("After charset translation:\n"+new_text)
    # Do the virama-reversal using a regular expression
    pattern = r"(.){0}".format(virama)
    repl = r"{0}\1".format(virama)
    new_text = re.sub(pattern, repl, new_text, flags=re.MULTILINE)
    if debug:
        print ("After viraama-reversal:\n"+new_text)
    return new_text

if __name__ == "__main__":
    print("Please enter the line of Devanagari to be converted to Bharati Braille")
    print("The Bharati Braille text is:\n"+convert_devanagari_to_braille(input()))
