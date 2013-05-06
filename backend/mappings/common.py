#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set sts=4 sw=4 et :

# Authors:
#  Nirbheek Chauhan <nirbheek.chauhan@gmail.com>
#  Pooja Saxena <anexasajoop@gmail.com>  

# License:
#  AGPL-3
#  http://www.gnu.org/licenses/agpl-3.0.html



################################
# Language-agnostic characters #
################################



# References and resources used:
# 1. Ahuja, Swaran (2012) Bharati Braille Shikshak. National Association for the Blind, Mumbai.
# 2. Unicode Code Chart for Braille Patterns Range: 2800–28FF [http://www.unicode.org/charts/PDF/U2800.pdf]
# 3. “Braille” on Wikipedia [http://en.wikipedia.org/wiki/Braille]



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

## ELLIPSIS
# Used for converting a "fake ellipsis" (...) as well. See converter.py
ellipsis = "⠠⠠⠠"

# This is placed separately because it shares braille characters with
# 'punctuation', and that's bad for a dictionary
paired_punctuation = {
     "⠦": ('“',), # Opening double quote (Sadharan avataran chinh)
     "⠴": ('”',), # Closing double quote (Sadharan avataran chinh)
     "⠠⠦": ('‘',), # Opening single quote (Aantariya avataran chinh)
     "⠴⠄": ('’',), # Closing single quote (Aantariya avataran chinh)
     "⠶": ("(", ")"), # Round brackets (Koshthak)
     "⠠⠶": ("[",), # Opening square bracket (Koshthak)
     "⠶⠄": ("]",), # Closing square bracket (Koshthak)
}

# Dumb quotes that we can't translate to bharati braille
dumb_quotes = ("'", '"');

## DASHES
# They need to be in a different variable
# Because they require the number symbol to be put before each number if they are put between two numbers.
# That is not the case with other punctuation symbols like the hyphen, mathematical comma (see below), apostrophe and _vakra rekha_
dashes = {
    "⠤": ("‐", "-"), # Hyphen and hyphen-minus,  "dash" (two-hyphens or en-dash), and "double dash" (four hyphens or em-dash)
    "⠤⠤": ("–",), # en-dash
    "⠤⠤⠤⠤": ("—",), # em-dash
}

## Heuristics
# Dumb (ASCII) quote detection?
# Forward slash between numbers (and otherwise) should trigger a warning, and skip the word
# Math symbols should trigger the math warning, and skip the equation
# Unencoded devanagari characters should trigger an unknown warning, and skip the word
# Unknown characters should trigger an unknown warning, and skip the word


####################
# Numbers and Math #
####################

## NUMBERS
# Ordered as Latin, Devanagari, Tamil, Gujarati, Bengali, Telugu
number_prefix = "⠼"
numbers = {
      "⠁": ("1", "१", "௧", "૧", "১", "౧"),  # One
      "⠃": ("2", "२", "௨", "૨", "২", "౨"),  # Two
      "⠉": ("3", "३", "௩", "૩", "৩", "౩"),  # Three
      "⠙": ("4", "४", "௪", "૪", "৪", "౪"),  # Four
      "⠑": ("5", "५", "௫", "૫", "৫", "౫"),  # Five
      "⠋": ("6", "६", "௬", "૬", "৬", "౬"),  # Six
      "⠛": ("7", "७", "௭", "૭", "৭", "౭"),  # Seven
      "⠓": ("8", "८", "௮", "૮", "৮", "౮"),  # Eight
      "⠊": ("9", "९", "௯", "૯", "৯", "౯"),  # Nine
      "⠚": ("0", "०", "௦", "૦", "০", "౦"),  # Zero
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