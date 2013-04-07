#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set sts=4 sw=4 et :
#
# Authors:
#  Nirbheek Chauhan <nirbheek.chauhan@gmail.com>
#  Pooja Saxena <anexasajoop@gmail.com>  
# License:
#  AGPL-3
#  http://www.gnu.org/licenses/agpl-3.0.html
#
# *A* mapping from Devanagari Unicode to Bharati Braille
# 
# References and resources used:
# * http://acharya.iitm.ac.in/disabilities/bh_brl.php
# * http://acharya.iitm.ac.in/cgi-bin/brcell_disp.pl?sanskrit
# * http://acharya.iitm.ac.in/demos/br_transcription.php
# * http://www.unicode.org/charts/PDF/U0900.pdf
# * http://libbraille.org/translator.php?table=hindi
#   ^ adds halanths at arbitrary places
# * http://rishida.net/scripts/uniview/
# * http://en.wikipedia.org/wiki/Braille_patterns


#################################################
# Devanagari Unicode to Bharati Braille Mapping #
#################################################

## VIRAMA
# This is used for the "virama-reversal". See converter.py.
virama = "⠈"

## SCHWA
# This is used for the consonant-vowel idiosyncracy. See converter.py
schwa = "⠁"

## ELLIPSIS
# Used for converting a "fake ellipsis" (...) as well. See converter.py
ellipsis = "⠠⠠⠠"

## PUNCTUATION
punctuation = {
     "⠂": (",",), # Comma (swalp-viraam)
     "⠆": (";",), # Semi-colon (ardh-viraam)
     "⠒": (":",), # Colon (apurn-viraam)
     "⠲": ("।",), # Devanagari single danda
     "⠲⠲": ("॥",), # Devanagari double danda
     "⠖": ("!",), # Exclamation point (udgar-chinh)
     "⠦": ("?",), # Question mark (prashn-chinh)
     "⠠⠠⠠": ("…",), # Ellipsis
     "⠔⠔": ("*",), # Asterisk 
}

paired_punctuation = {
     "⠦": ('“',), # Opening double quote (Sadharan avataran chinh)
     "⠴": ('”',), # Closing double quote (Sadharan avataran chinh)
     "⠠⠦": ('‘',), # Opening single quote (Aantariya avataran chinh)
     "⠴⠄": ('’',), # Closing single quote (Aantariya avataran chinh)
     "⠶": ("(", ")"), # Round brackets (Koshthak)
     "⠠⠶": ("[",), # Opening square bracket (Koshthak)
     "⠶⠄": ("]",), # Closing square bracket (Koshthak)
}

## DASHES
# They need to be in a different variable
# Because they require the number symbol to be put before each number if they are put between two numbers.
# That is not the case with other punctuation symbols like the hyphen, mathematical comma (see below), apostrophe and _vakra rekha_
dashes = {
    "⠤": ("‐", "-"), # Hyphen and hyphen-minus,  "dash" (two-hyphens or en-dash), and "double dash" (four hyphens or em-dash)
    "⠤⠤": ("–",), # en-dash
    "⠤⠤⠤⠤": ("—",), # em-dash
}

## NUMBERS
number_prefix = "⠼"
numbers = {
      "⠁": ("1",  "१"),  # 1
      "⠃": ("2",  "२"),  # 2
      "⠉": ("3",  "३"),  # 3
      "⠙": ("4",  "४"),  # 4
      "⠑": ("5",  "५"),  # 5
      "⠋": ("6",  "६"),  # 6
      "⠛": ("7",  "७"),  # 7
      "⠓": ("8",  "८"),  # 8
      "⠊": ("9",  "९"),  # 9
      "⠚": ("0",  "०"),  # 0
}

## MATHEMATICAL SYMBOLS
# NOTE: Completely ignored
math_symbols = {
      "⠬": ("+", ), # + (plus sign)
      "⠤": ("−", ), # − (minus sign)
      "⠈⠡": ("×", ), # × (multiplication sign)
      "⠨⠌": ("÷", ), # ÷ (division sign)
      "⠨⠅": ("=", ), # = (equal sign)
      "⠈⠴⠅": ("%", ), # % (percentage sign) 
}

## MATHEMATICAL PUNCTUATION
# Used when a comma is inside a long number to indicate places, like 1,500,000.
# In both these cases, the number sign (⠼) will only come once—right at the beginning
math_punctuation = {
  "⠠": (",",), # Same Braille character as the visarga
  "⠨": (".",), # Decimal point
}

## VARIOUS DEVANAGARI SIGNS
various_signs = {
     "⠈": ("्",), # Virama; it is repeated here because earlier no mapping is defined.
   #"⠂": ("ऽ",), # Avagraha (same mapping as comma?)
     "⠰": ("ं", "ँ",), # Anusvara and Chandra-bindu share a single Braille character
     "⠠": ("ः",), # Visarga
	 "": ("़",), # Nukta is being completely ignored (except for ड़ and ढ़)
}

## VOWELS AND VOWEL SIGNS
# In Bharati Braille, each vowel and its corresponding vowel sign (or matra) is represented by the same Braille character.
# If there is more than one devanagari character, make sure that the first is the vowel, and not the matra
vowels = {
     # The schwa vowel is inherent in every consonant, and does not have a separate vowel sign.
     "⠁": ("अ",), # This is repeated here because earlire no mapping is defined.
     "⠜": ("आ", "ा" ),
     "⠊": ("इ", "ि"),
     "⠔": ("ई", "ी"),
     "⠥": ("उ", "ु"),
     "⠳": ("ऊ", "ू"),
    # ॠ and ॄ have no direct mapping in Bharati Braille.
     "⠐⠗": ("ऋ", "ृ"),
     "⠢": ("ऍ", "ॅ"),
    # ऎ and ॆ have no direct mapping in Bharati Braille.
     "⠑": ("ए", "े",),
     "⠌": ("ऐ", "ै"),
     "⠭": ("ऑ","ॉ"),
    # ऒ and ॊ have no direct mapping in Bharati Braille.
     "⠕": ("ओ", "ो"),
     "⠪": ("औ", "ौ"),
} 

## CONSONANTS
consonants = {
    "⠅": ("क", "क़"),
     "⠨": ("ख", "ख़"),
     "⠛": ("ग", "ग़"),
     "⠣": ("घ",),
     "⠬": ("ङ",),
     "⠉": ("च",),
     "⠡": ("छ",),
    # Yes. This is not a mistake. JA and ZA are the same.
     "⠚": ("ज", "ज़"),
     "⠴": ("झ",),
     "⠒": ("ञ",),
     "⠾": ("ट",),
     "⠺": ("ठ",),
     "⠫": ("ड",),
     "⠿": ("ढ",),
     "⠼": ("ण",),
     "⠞": ("त",),
     "⠹": ("थ",),
     "⠙": ("द",),
     "⠮": ("ध",),
     "⠝": ("न", "ऩ"),
     "⠏": ("प",),
     "⠖": ("फ", "फ़"),
     "⠃": ("ब",),
     "⠘": ("भ",),
     "⠍": ("म",),
     "⠽": ("य", "य़",),
     "⠗": ("र", "ऱ"),
     "⠇": ("ल",),
     "⠸": ("ळ", "ऴ"),
     "⠧": ("व",),
     "⠩": ("श",),
     "⠯": ("ष",),
     "⠎": ("स",),
     "⠓": ("ह",),
# Nukta characters that have been assigned separate symbols in Braille
     "⠻": ("ड़",),
     "⠐⠻": ("ढ़",),
}

## AKHAND LIGATURES
# Akhand ligatures are consonantal ligatures that have a distinct visual form that may not contain the base forms.
# Some of these are represented as unique characters in Bharati Braille.
# They must be converted first; otherwise we'll get an expanded form of these conjuncts in the Braille transcription.
akhand = {
    # क्ष = क + ् + ष
     "⠟": ("क्ष",),
    # ज्ञ = ज + ् + ञ
     "⠱": ("ज्ञ",),
}

# TODO: More numbers shit on pg 36
# TODO: Fractions, pg 37
# TODO: Number symbol when using math signs (pg 39)

## Heuristics
# Dumb (ASCII) quote detection?
# Forward slash between numbers (and otherwise) should trigger a warning, and skip the word
# Math symbols should trigger the math warning, and skip the equation
# Unencoded devanagari characters should trigger an unknown warning, and skip the word
# Unknown characters should trigger an unknown warning, and skip the word

## Devanagari characters that have no mapping.
# This isn't used anywhere yet. It exists only for documentation.
# Haven't reviewed these yet.
_without_mapping = [
    # Characters which could be shoved somewhere else, just not sure where:
    ("ऄ", "ऌ", "ॡ", "ॢ", "ॣ", "ॻ", "ॼ", "ॾ", "ॿ", "ॽ"),
    # Characters without any mappings which can't be lumped anywhere else:
    ("ऀ", "ऺ", "ऻ", "़", "ॎ", "ॏ", "ॐ", "॑", "॒", "॓", "॔", "ॕ", "ॖ", "ॗ", "॰",
     "ॱ", "ॳ", "ॴ", "ॵ", "ॶ", "ॷ", "ॹ", "ॺ",),
    # Devanagari Extended; definitely no mappings:
    ("꣠", "꣡", "꣢", "꣣", "꣤", "꣥", "꣦", "꣧", "꣨", "꣩", "꣪", "꣫", "꣬", "꣭", "꣮",
     "꣯", "꣰", "꣱", ",ꣲ", "ꣳ", "ꣴ", "ꣵ", "ꣶ", "ꣷ", "꣸", "꣹", "꣺", "ꣻ"),
    # Vedic Extensions; definitely no mappings:
    ("᳐", "᳑", "᳒", "᳓", "᳔", "᳕", "᳖", "᳗", "᳘", "᳙", "᳚", "᳛", "᳜", "᳝", "᳞",
     "᳟", "᳠", "᳡", "᳢", "᳣", "᳤", "᳥", "᳦", "᳧", "᳨", "ᳩ", "ᳪ", "ᳫ", "ᳬ", "᳭",
     "ᳮ", "ᳯ", "ᳰ", "ᳱ", "ᳲ", "ᳳ", "᳴", "ᳵ", "ᳶ"),
]
