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

from mappings import virama, schwa
from mappings import akhand
from mappings import fake_ellipsis
from mappings import vowels, consonants, various_signs, dashes
from mappings import punctuation, paired_punctuation
from mappings import numbers, number_prefix
from mappings import math_punctuation
# We don't convert numbers and mathematical symbols yet
#from mappings import numbers, math_symbols

# sets of all consonants, and vowel characters.
# This list is used for the vowel idiosyncracy where 'अ' is placed explicitly 
# if a consonant is followed by a vowel character (not a vowel sign [matra])
all_consonants = set()
for each in consonants, akhand:
    for value in each.values():
        all_consonants.update(value)
vowel_chars = set()
for value in vowels.values():
    vowel_chars.add(value[0])
number_chars = set()
for value in numbers.values():
    number_chars.update(value)

# Characters that need to be converted in the first pass
priority_mappings = akhand
# Aggregate characters that are directly subsituted for their braille equivalents
simple_letter_mappings = {}
for each in vowels, consonants, various_signs, dashes:
    simple_letter_mappings.update(each)

# Reverse the braille-to-devanagari mapping.
# We need a devanagari-to-braille mapping
d_to_b = {}
for (braille, devanagari_list) in simple_letter_mappings.items():
    for each in devanagari_list:
        d_to_b[each] = braille
d_to_b_priority = {}
for (braille, devanagari_list) in priority_mappings.items():
    for each in devanagari_list:
        d_to_b_priority[each] = braille
d_to_b_punctuation = {}
for (braille, devanagari_list) in punctuation.items():
    for each in devanagari_list:
        d_to_b_punctuation[each] = braille
d_to_b_paired_punctuation = {}
for (braille, devanagari_list) in paired_punctuation.items():
    for each in devanagari_list:
        d_to_b_paired_punctuation[each] = braille
d_to_b_numbers = {}
for (braille, devanagari_list) in numbers.items():
    for each in devanagari_list:
        d_to_b_numbers[each] = braille
d_to_b_math_punctuation = {}
for (braille, devanagari_list) in math_punctuation.items():
    for each in devanagari_list:
        d_to_b_math_punctuation[each] = braille

def insert_explicit_schwa(text):
    # Create a regex pattern for matching vowel characters
    vowel_pattern = '[' + ''.join(vowel_chars) + ']'
    # For each vowel character found
    for each in re.finditer(vowel_pattern, text, flags=re.MULTILINE):
        # If it is preceded by a consonant
        if text[each.start()-1] in all_consonants:
            # Insert an explicit schwa (in Braille) for the consonant-vowel
            # idiosyncracy
            text = text[:each.start()] + schwa + text[each.start():]
    return text

def virama_reversal(text):
    # Do the virama-reversal using a regular expression
    # TODO: Compile this regular expression (for speed)
    pattern = r"(.){0}".format(virama)
    repl = r"{0}\1".format(virama)
    return re.sub(pattern, repl, text, flags=re.MULTILINE)

def translate_math(text):
    # This translates commas between numbers, such as: 1,500,000
    pattern = r"([{0}]+){1}([{0}]+)".format(''.join(number_chars), ",")
    repl = r"{0}\1{1}\2".format(number_prefix, d_to_b_math_punctuation[","])
    text = re.sub(pattern, repl, text, flags=re.MULTILINE)
    # This translates decimal points between numbers, such as: .5, .9
    pattern = r"([^{0}]+){1}([{0}]+)".format(''.join(number_chars), ".")
    repl = r"\1{0}{1}\2".format(number_prefix, d_to_b_math_punctuation["."])
    text = re.sub(pattern, repl, text, flags=re.MULTILINE)
    # This translates decimal points between numbers, such as: 0.5, 1.9
    pattern = r"([{0}]+){1}([{0}]+)".format(''.join(number_chars), ".")
    repl = r"{0}\1{1}\2".format(number_prefix, d_to_b_math_punctuation["."])
    text = re.sub(pattern, repl, text, flags=re.MULTILINE)
    # This translates numbers to braille characters
    text = text.translate(str.maketrans(d_to_b_numbers))
    return text

def convert_devanagari_to_braille(text, debug=False):
    """
    Converts the given text from Devanagari to Bharati Braille
    Leaves unknown characters untouched
    """
    new_text = text.replace(fake_ellipsis[1], fake_ellipsis[0])
    new_text = translate_math(new_text)
    if debug:
        print ("After math translation:\n"+new_text)
    new_text = insert_explicit_schwa(new_text)
    if debug:
        print ("After explicit-schwa conversion:\n"+new_text)
    # Do a string substitution for the string-to-char conversion
    for (key, value) in d_to_b_priority.items():
        new_text = new_text.replace(key, value)
    if debug:
        print ("After string-to-char conversion:\n"+new_text)
    # Create a translation table for unicode characters
    # This is faster than a string replacement
    new_text = new_text.translate(str.maketrans(d_to_b_punctuation))
    if debug:
        print ("After punctuation translation:\n"+new_text)
    new_text = new_text.translate(str.maketrans(d_to_b))
    if debug:
        print ("After charset translation:\n"+new_text)
    new_text = virama_reversal(new_text)
    if debug:
        print ("After viraama-reversal:\n"+new_text)
    return new_text

if __name__ == "__main__":
    print("Please enter the line of Devanagari to be converted to Bharati Braille")
    print("The Bharati Braille text is:\n"+convert_devanagari_to_braille(input()))
