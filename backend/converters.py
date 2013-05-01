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
# Converts Unicode Devanagari text to Bharati Braille using string translation
# and regular expressions.
#
# TODO: Compile the regular expressions used in this module to speed things up
#

import re
import sys

if sys.version_info.major != 3:
    raise Exception("This program needs Python 3!")

from mappings import virama, schwa, ellipsis
from mappings import akhand
from mappings import vowels, consonants, various_signs, dashes
from mappings import punctuation, paired_punctuation
from mappings import numbers, number_prefix
from mappings import math_punctuation
# TODO: Math symbols will be handled with a warning and passed through unchanged
#from mappings import numbers, math_symbols

# Sets of all consonants, and vowel characters.
# This list is used for the vowel idiosyncracy where 'अ' is placed explicitly 
# if a consonant is followed by a vowel character (not a vowel sign [matra])
# See: insert_explicit_schwa()
all_consonants = set()
for each in consonants, akhand:
    for value in each.values():
        all_consonants.update(value)
vowel_chars = set()
for value in vowels.values():
    length = len(value)
    # We assume here that the first value is a vowel char, the second is a
    # vowel sign, and that there are no more than two values
    if length == 2:
        vowel_chars.add(value[0])
    elif length > 2:
        raise Exception("Expected each Braille vowel to map from 2 Devanagari vowels, but it's mapping from more than 2?")

# Set of all numbers. Used in translate_math()
number_chars = set()
for value in numbers.values():
    number_chars.update(value)

# Consonants+vowels that need to be converted before simple_letter_mappings
priority_mappings = akhand
# List of consonants+vowels that are directly replaced with braille chars
simple_letter_mappings = {}
for each in vowels, consonants, various_signs, dashes:
    simple_letter_mappings.update(each)

# Reverse all the braille-to-devanagari mappings from mappings.py
# We need a devanagari-to-braille mapping for each type of mapping
d_to_b = {}
for (braille, devanagari_list) in simple_letter_mappings.items():
    for each in devanagari_list:
        d_to_b[each] = braille
d_to_b_priority = {}
for (braille, devanagari_list) in priority_mappings.items():
    for each in devanagari_list:
        d_to_b_priority[each] = braille
d_to_b_punctuation = {}
for (braille, devanagari_list) in punctuation.items() | paired_punctuation.items():
    for each in devanagari_list:
        d_to_b_punctuation[each] = braille
d_to_b_numbers = {}
for (braille, devanagari_list) in numbers.items():
    for each in devanagari_list:
        d_to_b_numbers[each] = braille
d_to_b_math_punctuation = {}
for (braille, devanagari_list) in math_punctuation.items():
    for each in devanagari_list:
        d_to_b_math_punctuation[each] = braille

def insert_explicit_schwa(text):
    # [consonant][vowel] -> [consonant][schwa][vowel]
    pattern = r"([{0}])([{1}])".format(''.join(all_consonants),
                                       ''.join(vowel_chars))
    repl = r"\1{0}\2".format(schwa)
    return re.sub(pattern, repl, text, flags=re.MULTILINE)

def virama_reversal(text):
    # Do the virama-reversal using a regular expression
    pattern = r"(.){0}".format(virama)
    repl = r"{0}\1".format(virama)
    return re.sub(pattern, repl, text, flags=re.MULTILINE)

def translate_math(text):
    # Add number prefix for such numbers:
    # 12876
    # 1,540,000
    # .5234
    # 2.8999
    # 8.8.8
    # Also adds a prefix for such numbers:
    # 5. (not a decimal)
    # 123, (not a number sequence)
    # ,999 (prefix inserted after the comma)
    # Which matches precisely what we need.
    pattern = r"(,?)([{0}.,]+)".format(''.join(number_chars))
    repl = r"\1{0}\2".format(number_prefix)
    text = re.sub(pattern, repl, text, flags=re.MULTILINE)
    # Translate commas for numbers such as: 1,500,000
    pattern = r"([{0}]+?){1}(?=[{0}]+?)".format(''.join(number_chars), ",")
    repl = r"\1{0}".format(d_to_b_math_punctuation[","])
    text = re.sub(pattern, repl, text, flags=re.MULTILINE)
    # Translate decimal points for numbers such as: .5
    pattern = r"(?=[^{0}]+?)?{1}([{0}]+?)".format(''.join(number_chars), "\.")
    repl = r"{0}\1".format(d_to_b_math_punctuation["."])
    text = re.sub(pattern, repl, text, flags=re.MULTILINE)
    # Translate decimal points for numbers such as: 0.5 and 1.0.5
    pattern = r"([{0}]+?){1}(?=[{0}]+?)".format(''.join(number_chars), "\.")
    repl = r"\1{0}".format(d_to_b_math_punctuation["."])
    text = re.sub(pattern, repl, text, flags=re.MULTILINE)
    # Translate numbers to braille characters without adding a number prefix
    text = text.translate(str.maketrans(d_to_b_numbers))
    return text

def convert_devanagari_to_braille(text, debug=False):
    """
    Converts the given text from Devanagari to Bharati Braille
    Leaves unknown characters untouched
    """
    # Convert a fake ellipsis (...) as well
    new_text = re.sub("(?=[^.]?)(\.\.\.)(?=[^.]?)", ellipsis, text)
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
