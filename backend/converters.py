#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set sts=4 sw=4 et tw=0 :
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
# TODO: Script detection is implemented very naïvely, and is slow as hell
#

import re
import sys

if sys.version_info.major != 3:
    raise Exception("This program needs Python 3!")

# Characters common to all encodings
from mappings.common import ellipsis, dashes, punctuation, paired_punctuation
from mappings.common import numbers, number_prefix, math_punctuation
# We warn when these are inputted
from mappings.common import dumb_quotes, math_symbols

# Devanagari mappings
from mappings.dv import dv_virama, dv_schwa, dv_composite_letters, dv_akhand
from mappings.dv import dv_vowels, dv_consonants, dv_various_signs
# Gujarati mappings
from mappings.gu import gu_virama, gu_schwa, gu_composite_letters, gu_akhand
from mappings.gu import gu_vowels, gu_consonants, gu_various_signs
# Bengali mappings
from mappings.bn import bn_virama, bn_schwa, bn_composite_letters, bn_akhand
from mappings.bn import bn_vowels, bn_consonants, bn_various_signs
# Telugu mappings
from mappings.te import te_virama, te_schwa, te_akhand
from mappings.te import te_vowels, te_consonants, te_various_signs
# Tamil mappings
from mappings.ta import ta_virama, ta_schwa, ta_akhand
from mappings.ta import ta_vowels, ta_consonants, ta_various_signs

BB_WARN_WRAPPER = """<p class="warning">{0}</p>\n"""
BB_WARN_DUMB_QUOTES = BB_WARN_WRAPPER.format("""The convertor does not handle <a href="about.html#conv_limitations">dumb quotes</a>.""")
BB_WARN_MATH_OPS = BB_WARN_WRAPPER.format("""The convertor does not handle <a href="about.html#conv_limitations">mathematical operators</a>.""")
# XXX: Link to contribute page?
BB_ERR_UNKNOWN_SCRIPT = BB_WARN_WRAPPER.format("""Unable to convert to Bharati Braille: Unknown script.""")
# TODO: Link to Bharati Braille limitation concerning multi-script text
BB_ERR_MANY_SCRIPTS = BB_WARN_WRAPPER.format("""Unable to convert to Bharati Braille: Multiple scripts in input.""")

def insert_explicit_schwa(text, schwa, all_consonants, vowel_chars, debug=False):
    "[consonant][vowel] -> [consonant][schwa][vowel]"
    pattern = r"([{0}])([{1}])".format(''.join(all_consonants),
                                       ''.join(vowel_chars))
    repl = r"\1{0}\2".format(schwa)
    new_text = re.sub(pattern, repl, text, flags=re.MULTILINE)
    if debug:
        print("After explicit-schwa conversion:\n"+new_text)
    return new_text


def virama_reversal(text, virama, debug=False):
    "Do the virama-reversal using a regular expression"
    pattern = r"(.){0}".format(virama)
    repl = r"{0}\1".format(virama)
    new_text = re.sub(pattern, repl, text, flags=re.MULTILINE)
    if debug:
        print("After viraama-reversal:\n"+new_text)
    return new_text


def translate_math(text, debug=False):
    """
    Add number prefix for such numbers:
     12876
     1,540,000
     .5234
     2.8999
     8.8.8
    Also adds a prefix for such numbers:
     5. (not a decimal)
     123, (not a number sequence)
     ,999 (prefix inserted after the comma)
    Which matches precisely what we need.
    """
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
        print("After math translation:\n"+text)
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
        warnings += BB_WARN_WRAPPER.format(BB_WARN_DUMB_QUOTES)
    if text_set.intersection(all_math_symbols):
        warnings += BB_WARN_WRAPPER.format(BB_WARN_MATH_OPS)
    return warnings

def convert_indic_to_braille(text, schwa, virama, all_consonants,
                             vowel_chars, indic_to_bb, indic_to_bb_composite,
                             debug=False):
    """
    Converts the given text from the given Indic language to Bharati Braille
    Leaves unknown characters untouched
    
    The order of conversion *has* to be:
    1. Insert explicit schwa
    2. Replace akhand characters
    3. Substitude vowels and consonants
    4. Replace numbers, punctuation, etc.
    5. Append warnings
    """
    new_text = text[:]
    new_text = insert_explicit_schwa(new_text, schwa, all_consonants,
                                     vowel_chars, debug)
    # Do str.replace instead of str.maketrans for the string-to-char conversion
    for (key, value) in indic_to_bb_composite.items():
        new_text = new_text.replace(key, value)
    if debug:
        print("After string-to-char conversion:\n"+new_text)
    new_text = new_text.translate(str.maketrans(indic_to_bb))
    if debug:
        print("After charset translation:\n"+new_text)
    new_text = virama_reversal(new_text, virama)
    new_text = convert_common_glyphs_to_braille (new_text, debug)
    warnings = append_warnings(new_text)
    return (new_text, warnings)

def convert_devanagari_to_braille(text, debug=False):
    return convert_indic_to_braille(text, dv_schwa, dv_virama,
                                    all_dv_consonants, dv_vowel_chars,
                                    dv_to_bb, dv_to_bb_composite, debug)

def convert_gujarati_to_braille(text, debug=False):
    return convert_indic_to_braille(text, gu_schwa, gu_virama,
                                    all_gu_consonants, gu_vowel_chars,
                                    gu_to_bb, gu_to_bb_composite, debug)

def convert_bengali_to_braille(text, debug=False):
    return convert_indic_to_braille(text, bn_schwa, bn_virama,
                                    all_bn_consonants, bn_vowel_chars,
                                    bn_to_bb, bn_to_bb_composite, debug)

def convert_telugu_to_braille(text, debug=False):
    return convert_indic_to_braille(text, te_schwa, te_virama,
                                    all_te_consonants, te_vowel_chars,
                                    te_to_bb, te_to_bb_composite, debug)

def convert_tamil_to_braille(text, debug=False):
    return convert_indic_to_braille(text, ta_schwa, ta_virama,
                                    all_ta_consonants, ta_vowel_chars,
                                    ta_to_bb, ta_to_bb_composite, debug)

def _no_braille_converter_found(text, debug=False):
    if debug:
        print("No braille converter found for: {0}".format(text))
    return ("", BB_ERR_UNKNOWN_SCRIPT)

def _multiple_braille_converters_found(text, debug=False):
    if debug:
        print("Multiple converters found for: {0}".format(text))
    return ("", BB_ERR_MANY_SCRIPTS)

def convert_any_indic_to_braille(text, debug=False):
    """
    Detects the indic script in use and uses the mapping matching that.

    If more than one indic script is detected in the text, throws an error and
    returns no output
    """
    text_set = frozenset(text)
    indic_converter = None
    # TODO: This is implemented in a very naïve manner and has bad O complexity
    for charset, converter in converters.items():
        if text_set & charset:
            if indic_converter:
                indic_converter = _multiple_braille_converters_found
                break
            indic_converter = converter
    if not indic_converter:
        indic_converter = _no_braille_converter_found
    return indic_converter(text, debug)

def _perform_mapping_pre_processing(consonants, vowels, akhand, composite_letters, various_signs):
    """
    Sets of all consonants and vowel *characters* (not maatras).
    This list is used for the vowel idiosyncracy where 'LETTER A' is placed 
    explicitly if a consonant is followed by a vowel character 
    (not a vowel sign, which is a 'maatra')
    See: insert_explicit_schwa()
    """
    all_consonants = set()
    for each in consonants, akhand, composite_letters:
        for value in each.values():
            all_consonants.update(value)
    vowel_chars = set()
    all_consonants_and_vowels = set(all_consonants)
    for value in vowels.values():
        all_consonants_and_vowels.update(value)
        length = len(value)
        # We assume here that the first value is a vowel char, the second is a
        # vowel sign, and that there are no more than two values
        if length == 2:
            vowel_chars.add(value[0])
        elif length > 2:
            raise Exception("Expected each Braille vowel to map from 2 vowels, but it's mapping from more than 2:\n{0}".format(vowels))
    # Reverse all the braille-to-indic mappings from mappings.py
    # We need a indic-to-bharati-braille mapping for each type of mapping
    indic_to_bb = {}
    for (braille, indic_list) in vowels.items() | consonants.items() | \
                                 various_signs.items() | dashes.items():
        for each in indic_list:
            indic_to_bb[each] = braille
    indic_to_bb_composite = {}
    for (braille, devanagari_list) in akhand.items() | composite_letters.items():
        for each in devanagari_list:
            indic_to_bb_composite[each] = braille
    return (all_consonants, frozenset(all_consonants_and_vowels), 
            vowel_chars, indic_to_bb, indic_to_bb_composite)

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
#    BEGIN INDIC   #
#  PRE-PROCESSING  #
####################
(all_dv_consonants, all_dv_consonants_and_vowels,
 dv_vowel_chars, dv_to_bb, dv_to_bb_composite) = \
        _perform_mapping_pre_processing(dv_consonants, dv_vowels, dv_akhand,
                                        dv_composite_letters, dv_various_signs)
(all_gu_consonants, all_gu_consonants_and_vowels,
 gu_vowel_chars, gu_to_bb, gu_to_bb_composite) = \
        _perform_mapping_pre_processing(gu_consonants, gu_vowels, gu_akhand,
                                        gu_composite_letters, gu_various_signs)
(all_bn_consonants, all_bn_consonants_and_vowels,
 bn_vowel_chars, bn_to_bb, bn_to_bb_composite) = \
        _perform_mapping_pre_processing(bn_consonants, bn_vowels, bn_akhand, 
                                        bn_composite_letters, bn_various_signs)
(all_te_consonants, all_te_consonants_and_vowels,
 te_vowel_chars, te_to_bb, te_to_bb_composite) = \
        _perform_mapping_pre_processing(te_consonants, te_vowels, te_akhand,
                                        {}, te_various_signs)
(all_ta_consonants, all_ta_consonants_and_vowels,
 ta_vowel_chars, ta_to_bb, ta_to_bb_composite) = \
        _perform_mapping_pre_processing(ta_consonants, ta_vowels, ta_akhand,
                                        {}, ta_various_signs)
converters = {all_dv_consonants_and_vowels: convert_devanagari_to_braille,
              all_gu_consonants_and_vowels: convert_gujarati_to_braille,
              all_bn_consonants_and_vowels: convert_bengali_to_braille,
              all_te_consonants_and_vowels: convert_telugu_to_braille,
              all_ta_consonants_and_vowels: convert_tamil_to_braille,}
######################
# END PRE-PROCESSING #
######################

if __name__ == "__main__":
    print("Please enter the line of Indic text to be converted to Bharati Braille")
    print("The Bharati Braille text is:\n{0}\n{1}".format(*convert_any_indic_to_braille(input())))
