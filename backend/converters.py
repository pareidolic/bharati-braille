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
# Converts Unicode Devanagari text to Bharati Braille using string translation,
# text replacement, and regular expressions. The speed of these operations is:
#
# str.maketrans (faster than) str.replace (faster than) re.sub
#
# TODO: Compile the regular expressions used in this module to speed things up
#

import re
import sys

if sys.version_info.major != 3:
    raise Exception("This program needs Python 3!")

# Characters common to all encodings
from mappings import ellipsis, dashes, punctuation, paired_punctuation
from mappings import numbers, number_prefix, math_punctuation
# We warn when these are inputted
from mappings import dumb_quotes, math_symbols

# Devanagari mappings
from mappings import dv_virama, dv_schwa
from mappings import dv_akhand
from mappings import dv_vowels, dv_consonants, dv_various_signs
# Gujarati mappings
from mappings import gj_virama, gj_schwa
from mappings import gj_akhand
from mappings import gj_vowels, gj_consonants, gj_various_signs
# Bengali mappings
from mappings import bn_virama, bn_schwa
from mappings import bn_akhand
from mappings import bn_vowels, bn_consonants, bn_various_signs

######################
# BEGIN COMMON GLYPH #
#   PRE-PROCESSING   #
######################
# Set of all numbers. Used in translate_math()
number_chars = set()
for value in numbers.values():
    number_chars.update(value)

# Set of all math symbols
all_math_symbols = set()
for value in math_symbols.values():
    all_math_symbols.update(value)

# Reverse all the bharati-braille-to-glyph mappings from mappings.py
# We need a glyph-to-bharati-braille mapping for each type of mapping
# This section converts all the characters common for all Indic scripts
cm_to_bb_punctuation = {}
for (braille, devanagari_list) in punctuation.items() | \
                                  paired_punctuation.items() | dashes.items():
    for each in devanagari_list:
        cm_to_bb_punctuation[each] = braille
cm_to_bb_numbers = {}
for (braille, devanagari_list) in numbers.items():
    for each in devanagari_list:
        cm_to_bb_numbers[each] = braille
cm_to_bb_math_punctuation = {}
for (braille, devanagari_list) in math_punctuation.items():
    for each in devanagari_list:
        cm_to_bb_math_punctuation[each] = braille

####################
# BEGIN DEVANAGARI #
#  PRE-PROCESSING  #
####################
# Sets of all Devanagari consonants, and vowel characters.
# This list is used for the vowel idiosyncracy where 'अ' is placed explicitly 
# if a consonant is followed by a vowel character (not a vowel sign [matra])
# See: insert_explicit_schwa()
all_dv_consonants = set()
for each in dv_consonants, dv_akhand:
    for value in each.values():
        all_dv_consonants.update(value)
dv_vowel_chars = set()
for value in dv_vowels.values():
    length = len(value)
    # We assume here that the first value is a vowel char, the second is a
    # vowel sign, and that there are no more than two values
    if length == 2:
        dv_vowel_chars.add(value[0])
    elif length > 2:
        raise Exception("Expected each Braille vowel to map from 2 Devanagari vowels, but it's mapping from more than 2?")

# Reverse all the braille-to-devanagari mappings from mappings.py
# We need a devanagari-to-bharati-braille mapping for each type of mapping
dv_to_bb = {}
for (braille, devanagari_list) in dv_vowels.items() | dv_consonants.items() | \
                                  dv_various_signs.items() | dashes.items():
    for each in devanagari_list:
        dv_to_bb[each] = braille
dv_to_bb_akhand = {}
for (braille, devanagari_list) in dv_akhand.items():
    for each in devanagari_list:
        dv_to_bb_akhand[each] = braille

##################
# BEGIN GUJARATI #
# PRE-PROCESSING #
##################
# Sets of all Gujarati consonants, and vowel characters.
# This list is used for the vowel idiosyncracy where 'अ' is placed explicitly 
# if a consonant is followed by a vowel character (not a vowel sign [matra])
# See: insert_explicit_schwa()
all_gj_consonants = set()
for each in gj_consonants, gj_akhand:
    for value in each.values():
        all_gj_consonants.update(value)
gj_vowel_chars = set()
for value in gj_vowels.values():
    length = len(value)
    # We assume here that the first value is a vowel char, the second is a
    # vowel sign, and that there are no more than two values
    if length == 2:
        gj_vowel_chars.add(value[0])
    elif length > 2:
        raise Exception("Expected each Braille vowel to map from 2 Gujarati vowels, but it's mapping from more than 2?")

# Reverse all the braille-to-devanagari mappings from mappings.py
# We need a devanagari-to-bharati-braille mapping for each type of mapping
gj_to_bb = {}
for (braille, devanagari_list) in gj_vowels.items() | gj_consonants.items() | \
                                  gj_various_signs.items():
    for each in devanagari_list:
        gj_to_bb[each] = braille
gj_to_bb_akhand = {}
for (braille, devanagari_list) in gj_akhand.items():
    for each in devanagari_list:
        gj_to_bb_akhand[each] = braille

##################
# BEGIN BENGALI  #
# PRE-PROCESSING #
##################
# Sets of all Bengali consonants, and vowel characters.
# This list is used for the vowel idiosyncracy where 'अ' is placed explicitly 
# if a consonant is followed by a vowel character (not a vowel sign [matra])
# See: insert_explicit_schwa()
all_bn_consonants = set()
for each in bn_consonants, bn_akhand:
    for value in each.values():
        all_bn_consonants.update(value)
bn_vowel_chars = set()
for value in bn_vowels.values():
    length = len(value)
    # We assume here that the first value is a vowel char, the second is a
    # vowel sign, and that there are no more than two values
    if length == 2:
        bn_vowel_chars.add(value[0])
    elif length > 2:
        raise Exception("Expected each Braille vowel to map from 2 Gujarati vowels, but it's mapping from more than 2?")

# Reverse all the braille-to-devanagari mappings from mappings.py
# We need a devanagari-to-bharati-braille mapping for each type of mapping
bn_to_bb = {}
for (braille, devanagari_list) in bn_vowels.items() | bn_consonants.items() | \
                                  bn_various_signs.items():
    for each in devanagari_list:
        bn_to_bb[each] = braille
bn_to_bb_akhand = {}
for (braille, devanagari_list) in bn_akhand.items():
    for each in devanagari_list:
        bn_to_bb_akhand[each] = braille
######################
# END PRE-PROCESSING #
######################

def insert_explicit_schwa(text, schwa, all_consonants, vowel_chars, debug=False):
    # [consonant][vowel] -> [consonant][schwa][vowel]
    pattern = r"([{0}])([{1}])".format(''.join(all_consonants),
                                       ''.join(vowel_chars))
    repl = r"\1{0}\2".format(schwa)
    new_text = re.sub(pattern, repl, text, flags=re.MULTILINE)
    if debug:
        print("After explicit-schwa conversion:\n"+new_text)
    return new_text

def virama_reversal(text, virama, debug=False):
    # Do the virama-reversal using a regular expression
    pattern = r"(.){0}".format(virama)
    repl = r"{0}\1".format(virama)
    new_text = re.sub(pattern, repl, text, flags=re.MULTILINE)
    if debug:
        print("After viraama-reversal:\n"+new_text)
    return new_text

def translate_math(text, debug=False):
    ## Add number prefix for such numbers:
    # 12876
    # 1,540,000
    # .5234
    # 2.8999
    # 8.8.8
    ## Also adds a prefix for such numbers:
    # 5. (not a decimal)
    # 123, (not a number sequence)
    # ,999 (prefix inserted after the comma)
    ## Which matches precisely what we need.
    #
    ## Match something that:
    ## * Is a number «[{0}]+»
    ## * Number may start with a decimal point
    ## * Number may contain commas and/or more decimal points.
    pattern = r"(\.?[{0}]+[{0}\.,]*)".format(''.join(number_chars))
    repl = r"{0}\1".format(number_prefix)
    text = re.sub(pattern, repl, text, flags=re.MULTILINE)
    # Translate commas for numbers such as: 1,500,000
    pattern = r"([{0}]+?){1}(?=[{0}]+?)".format(''.join(number_chars), ",")
    repl = r"\1{0}".format(cm_to_bb_math_punctuation[","])
    text = re.sub(pattern, repl, text, flags=re.MULTILINE)
    # Translate decimal points for numbers such as: .5
    pattern = r"(?=[^{0}]+?)?{1}([{0}]+?)".format(''.join(number_chars), "\.")
    repl = r"{0}\1".format(cm_to_bb_math_punctuation["."])
    text = re.sub(pattern, repl, text, flags=re.MULTILINE)
    # Translate decimal points for numbers such as: 0.5 and 1.0.5
    pattern = r"([{0}]+?){1}(?=[{0}]+?)".format(''.join(number_chars), "\.")
    repl = r"\1{0}".format(cm_to_bb_math_punctuation["."])
    text = re.sub(pattern, repl, text, flags=re.MULTILINE)
    # Translate numbers to braille characters without adding a number prefix
    text = text.translate(str.maketrans(cm_to_bb_numbers))
    if debug:
        print("After math translation:\n"+new_text)
    return text

def convert_common_glyphs_to_braille(text, debug=False):
    new_text = text[:]
    # Convert a fake ellipsis (...) as well
    new_text = re.sub("(?=[^.]?)(\.\.\.)(?=[^.]?)", ellipsis, new_text)
    new_text = translate_math(new_text, debug)
    new_text = new_text.translate(str.maketrans(cm_to_bb_punctuation))
    if debug:
        print("After common glyph translation:\n"+new_text)
    return new_text

def append_warnings(text):
    # Warn about unhandled stuff
    warnings = ""
    text_set = set(text)
    if text_set.intersection(set(dumb_quotes)):
        warnings += """<p class="warning">The convertor does not handle <a href="about.html#conv_limitations">dumb quotes</a>.</p>\n"""
    if text_set.intersection(all_math_symbols):
        warnings += """<p class="warning">The convertor does not handle <a href="about.html#conv_limitations">mathematical operators</a>.</p>\n"""
    if warnings:
        warnings += "<br/>"
    return warnings

def convert_devanagari_to_braille(text, debug=False):
    """
    Converts the given text from Devanagari to Bharati Braille
    Leaves unknown characters untouched
    
    The order of conversion *has* to be:
    1. Insert explicit schwa
    2. Replace akhand characters
    3. Substitude vowels and consonants
    4. Replace numbers, punctuation, etc.
    5. Append warnings
    """
    new_text = text[:]
    new_text = insert_explicit_schwa(new_text, dv_schwa, all_dv_consonants,
                                     dv_vowel_chars, debug)
    # Do str.replace instead of str.maketrans for the string-to-char conversion
    for (key, value) in dv_to_bb_akhand.items():
        new_text = new_text.replace(key, value)
    if debug:
        print("After string-to-char conversion:\n"+new_text)
    new_text = new_text.translate(str.maketrans(dv_to_bb))
    if debug:
        print("After charset translation:\n"+new_text)
    new_text = virama_reversal(new_text, dv_virama)
    new_text = convert_common_glyphs_to_braille (new_text, debug)
    warnings = append_warnings(new_text)
    return (new_text, warnings)

def convert_gujarati_to_braille(text, debug=False):
    """
    Converts the given text from Gujarati to Bharati Braille
    Leaves unknown characters untouched
    """
    new_text = text[:]
    new_text = insert_explicit_schwa(new_text, gj_schwa, all_gj_consonants,
                                     gj_vowel_chars, debug)
    # Do str.replace instead of str.maketrans for the string-to-char conversion
    for (key, value) in gj_to_bb_akhand.items():
        new_text = new_text.replace(key, value)
    if debug:
        print("After string-to-char conversion:\n"+new_text)
    new_text = new_text.translate(str.maketrans(gj_to_bb))
    if debug:
        print("After charset translation:\n"+new_text)
    new_text = virama_reversal(new_text, gj_virama, debug)
    new_text = convert_common_glyphs_to_braille (new_text, debug)
    warnings = append_warnings(new_text)
    return (new_text, warnings)

def convert_bengali_to_braille(text, debug=False):
    """
    Converts the given text from Bengali to Bharati Braille
    Leaves unknown characters untouched
    """
    new_text = text[:]
    new_text = insert_explicit_schwa(new_text, bn_schwa, all_bn_consonants,
                                     bn_vowel_chars, debug)
    # Do str.replace instead of str.maketrans for the string-to-char conversion
    for (key, value) in bn_to_bb_akhand.items():
        new_text = new_text.replace(key, value)
    if debug:
        print("After string-to-char conversion:\n"+new_text)
    new_text = new_text.translate(str.maketrans(bn_to_bb))
    if debug:
        print("After charset translation:\n"+new_text)
    new_text = virama_reversal(new_text, bn_virama, debug)
    new_text = convert_common_glyphs_to_braille (new_text, debug)
    warnings = append_warnings(new_text)
    return (new_text, warnings)

if __name__ == "__main__":
    print("Please enter the line of Devanagari to be converted to Bharati Braille")
    print("The Bharati Braille text is:\n"+convert_devanagari_to_braille(input()))
