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


################################
# Language-agnostic characters #
################################

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
# Ordered as Latin, Devanagari, Tamil, Gujarati, Bengali
number_prefix = "⠼"
numbers = {
      "⠁": ("1", "१", "૧", "১"),  # One
      "⠃": ("2", "२", "૨", "২"),  # Two
      "⠉": ("3", "३", "૩", "৩"),  # Three
      "⠙": ("4", "४", "૪", "৪"),  # Four
      "⠑": ("5", "५", "૫", "৫"),  # Five
      "⠋": ("6", "६", "૬", "৬"),  # Six
      "⠛": ("7", "७", "૭", "৭"),  # Seven
      "⠓": ("8", "८", "૮", "৮"),  # Eight
      "⠊": ("9", "९", "૯", "৯"),  # Nine
      "⠚": ("0", "०", "૦", "০"),  # Zero
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

# TODO: More numbers shit on pg 36
# TODO: Fractions, pg 37
# TODO: Number symbol when using math signs (pg 39)


##############################################
# Bengali Unicode to Bharati Braille Mapping #
##############################################

## VIRAMA
# This is used for the "virama-reversal". See converter.py.
bn_virama = "⠈"

## SCHWA
# This is used for the "consonant-vowel idiosyncracy". See converter.py
bn_schwa = "⠁"

## VARIOUS SIGNS
# Various signs added here as Unicode escape codes because several scripts
# have the same signs, and they look very similar as well.
# Done to ensure accuracy.
bn_various_signs = {
    "⠈": ("\u09CD",), #Virama
    "⠂": ("\u09BD",), # Avagraha (same mapping as comma?)
    "⠄": ("\u0981",), # Chandra-bindu
    "⠰": ("\u0982",), # Anusvara    
    "⠠": ("\u0983",), # Visarga
    "": ("\u09BC",), # No Braille cell assigned for Bengali Nukta
}

## VOWELS AND VOWEL SIGNS
# In Bharati Braille, each vowel and its corresponding vowel sign (or matra) 
# is represented by the same Braille character.
bn_vowels = {
     # The schwa vowel is inherent in every consonant, and does not have a separate vowel sign.
     "⠁": ("অ",), # Letter A
     "⠜": ("আ", "া" ), # Letter AA
     "⠊": ("ই", "ি"), # Letter I
     "⠔": ("ঈ", "ী"), # Letter II
     "⠥": ("উ", "ু"), # Letter U
     "⠳": ("ঊ", "ূ"), # Letter UU
     "⠐⠗": ("ঋ", "ৃ"), # Letter Vocalic R
     "⠐⠇": ("ঌ","ৢ"), # Letter Vocalic L
     "⠑": ("এ", "ে",), # Letter E
     "⠌": ("ঐ", "ৈ"), # Letter AI
     "⠕": ("ও", "ो"), # Letter O
     "⠪": ("ঔ", "ौ"), # Letter AU
} 

## CONSONANTS
bn_consonants = {
     "⠅": ("ক",), # Letter KA
     "⠨": ("খ",), # Letter KHA
     "⠛": ("গ",), # Letter GA
     "⠣": ("ঘ",), # Letter GHA
     "⠬": ("ঙ",), # Letter NGA
     "⠉": ("চ",), # Letter CA
     "⠡": ("ছ",), # Letter CHA
     "⠚": ("জ",), # Letter JA
     "⠴": ("ঝ",), # Letter JHA
     "⠒": ("ঞ",), # Letter NYA
     "⠾": ("ট",), # Letter TTA
     "⠺": ("ঠ",), # Letter TTHA
     "⠫": ("ড",), # Letter DDA
     "⠿": ("ঢ",), # Letter DDHA
     "⠼": ("ণ",), # Letter NNA
     "⠞": ("ত",), # Letter TA
     "⠹": ("থ",), # Letter THA
     "⠙": ("দ",), # Letter DA
     "⠮": ("ধ",), # Letter DHA
     "⠝": ("ন",), # Letter NA
     "⠏": ("প",), # Letter PA
     "⠖": ("ফ",), # Letter PHA
     "⠃": ("ব",), # Letter BA
     "⠘": ("ভ",), # Letter BHA
     "⠍": ("ম",), # Letter MA
     "⠽": ("য",), # Letter YA
     "⠗": ("র",), # Letter RA
     "⠇": ("ল",), # Letter LA
     "⠧": ("ব",), ## Are Bengali BA and VA represented by the same letter? Reference needed. ##
     "⠩": ("শ",), # Letter SHA
     "⠯": ("ষ",), # Letter SSA
     "⠎": ("স",), # Letter SA
     "⠓": ("হ",), # Letter HA
# Nukta characters that have been assigned separate symbols in Braille
     "⠻": ("ড়",), # Letter RRA
     "⠐⠻": ("ঢ়",), # Letter RHA
     "⠢": ("য়",) # Letter YYA
}

## AKHAND LIGATURES
# Akhand ligatures are consonantal ligatures that have a distinct visual form that may not contain the base forms.
# Some of these are represented as unique characters in Bharati Braille.
# They must be converted first; otherwise we'll get an expanded form of these conjuncts in the Braille transcription.
bn_akhand = {
    # ক্ষ = ক + ্ + ষ
     "⠟": ("ক্ষ",),
    # জ্ঞ = জ + ্ + ঞ
     "⠱": ("জ্ঞ",),
}



###############################################
# Gujarati Unicode to Bharati Braille Mapping #
###############################################

## VIRAMA
# This is used for the "virama-reversal". See converter.py.
gj_virama = "⠈"

## SCHWA
# This is used for the consonant-vowel idiosyncracy. See converter.py
gj_schwa = "⠁"

## VOWELS AND VOWEL SIGNS
# In Bharati Braille, vowels and their corresponding
# vowel signs are represented by the same Braille pattern.
gj_vowels = {
     "⠁": ("અ",), 
     "⠜": ("આ", "ા" ),
     "⠊": ("ઇ", "િ"),
     "⠔": ("ઈ", "ી"),
     "⠥": ("ઉ", "ુ"),
     "⠳": ("ઊ", "ૂ"),
     "⠐⠗": ("ઋ", "ૃ"),
     "⠠⠗": ("ૠ", "ૄ"), 
     "⠢": ("ઍ", "ૅ"),
     "⠑": ("એ", "ે",),
     "⠌": ("ઐ", "ૈ"),
     "⠭": ("ઑ","ૉ"),
     "⠕": ("ઓ", "ો"),
     "⠪": ("ઔ", "ૌ"),
} 

## CONSONANTS
gj_consonants = {
    "⠅": ("ક",),
     "⠨": ("ખ",),
     "⠛": ("ગ",),
     "⠣": ("ઘ",),
     "⠬": ("ઙ",),
     "⠉": ("ચ",),
     "⠡": ("છ",),
     "⠚": ("જ",),
     "⠴": ("ઝ",),
     "⠒": ("ઞ",),
     "⠾": ("ટ",),
     "⠺": ("ઠ",),
     "⠫": ("ડ",),
     "⠿": ("ઢ",),
     "⠼": ("ણ",),
     "⠞": ("ત",),
     "⠹": ("થ",),
     "⠙": ("દ",),
     "⠮": ("ધ",),
     "⠝": ("ન",),
     "⠏": ("પ",),
     "⠖": ("ફ",),
     "⠃": ("બ",),
     "⠘": ("ભ",),
     "⠍": ("મ",),
     "⠽": ("ય",),
     "⠗": ("ર",),
     "⠇": ("લ",),
     "⠸": ("ળ",),
     "⠧": ("વ",),
     "⠩": ("શ",),
     "⠯": ("ષ",),
     "⠎": ("સ",),
     "⠓": ("હ",),
}

## VARIOUS SIGNS
# Various signs added here as Unicode escape codes because several scripts
# have the same signs, and they look very similar as well.
# Done to ensure accuracy.
gj_various_signs = {
    "⠈": ("\u0ACD",), #Virama
    "⠂": ("\u0ABD",), # Avagraha (same mapping as comma?)
    "⠄": ("\u0A81",), # Chandra-bindu
    "⠰": ("\u0A82",), # Anusvara    
    "⠠": ("\u0A83",), # Visarga
    "": ("\u0ABC",), # No Braille cell assigned for Gujarati Nukta
}

## AKHAND LIGATURES
# Akhand ligatures are consonantal ligatures that have a distinct visual form that may not contain the base forms.
# Some of these are represented as unique characters in Bharati Braille.
# They must be converted first; otherwise we'll get an expanded form of these conjuncts in the Braille transcription.
gj_akhand = {
    # ક્ષ = ક + ્ + ષ
     "⠟": ("ક્ષ",),
    # જ્ઞ = જ + ્ + ઞ
     "⠱": ("જ્ઞ",),
}

## WITHOUT MAPPING
# Characters in the Gujarati Unicode chart that haven't
# been assigned in Bharati Braille
gj_without_mapping = {
    "ઌ", "ૐ", "ૡ", "ૢ", "ૣ", "૰", "૱"
}

#################################################
# Devanagari Unicode to Bharati Braille Mapping #
#################################################

## VIRAMA
# This is used for the "virama-reversal". See converter.py.
dv_virama = "⠈"

## SCHWA
# This is used for the consonant-vowel idiosyncracy. See converter.py
dv_schwa = "⠁"


## VARIOUS SIGNS
# Various signs added here as Unicode escape codes because several scripts
# have the same signs, and they look very similar as well.
# Done to ensure accuracy.
dv_various_signs = {
    "⠈": ("\u094D",), #Virama; it is repeated here because earlier no mapping is defined.
    "⠂": ("\u093D",), # Avagraha (same mapping as comma?)
    "⠄": ("\u0901",), # Chandra-bindu
    "⠰": ("\u0902",), # Anusvara    
    "⠠": ("\u0903",), # Visarga
    "": ("\u093C",), # Nukta is being completely ignored (except for ड़ and ढ़)
}

## VOWELS AND VOWEL SIGNS
# In Bharati Braille, each vowel and its corresponding vowel sign (or matra) is represented by the same Braille character.
# If there is more than one devanagari character, make sure that the first is the vowel, and not the matra
dv_vowels = {
     # The schwa vowel is inherent in every consonant, and does not have a separate vowel sign.
     "⠁": ("अ",), # Letter A; This is repeated here because earlier no mapping is defined.
     "⠜": ("आ", "ा" ), # Letter AA
     "⠊": ("इ", "ि"), # Letter I
     "⠔": ("ई", "ी"), # Letter II
     "⠥": ("उ", "ु"), # Letter U
     "⠳": ("ऊ", "ू"), # Letter UU
     "⠐⠗": ("ऋ", "ृ"), # Letter Vocalic R
     "⠠⠗": ("ॠ","ॄ"), # Letter Vocalic RR
     "⠐⠇": ("ऌ","ॢ"), # Letter Vocalic L
     "⠠⠇": ("ॡ","ॣ"), # Letter Vocalic LL
     "⠢": ("ऍ", "ॅ"), # Letter Candra E
    # ऎ and ॆ have no direct mapping in Bharati Braille.
     "⠑": ("ए", "े",), # Letter E
     "⠌": ("ऐ", "ै"), # Letter AI
     "⠭": ("ऑ","ॉ"), # Letter Candra O
    # ऒ and ॊ have no direct mapping in Bharati Braille.
     "⠕": ("ओ", "ो"), # Letter O
     "⠪": ("औ", "ौ"), # Letter AU
} 

## CONSONANTS
dv_consonants = {
    "⠅": ("क", "क़"), # Letter KA and QA
     "⠨": ("ख", "ख़"), # Letter KHA and KHHA
     "⠛": ("ग", "ग़"), # Letter GA and GHHA
     "⠣": ("घ",), # Letter GHA
     "⠬": ("ङ",), # Letter NGA
     "⠉": ("च",), # Letter CA
     "⠡": ("छ",), # Letter CHA
     "⠚": ("ज", "ज़"), # Letter JA and ZA
     "⠴": ("झ",), # Letter JHA
     "⠒": ("ञ",), # Letter NYA
     "⠾": ("ट",), # Letter TTA
     "⠺": ("ठ",), # Letter TTHA
     "⠫": ("ड",), # Letter DDA
     "⠿": ("ढ",), # Letter DDHA
     "⠼": ("ण",), # Letter NNA
     "⠞": ("त",), # Letter TA
     "⠹": ("थ",), # Letter THA
     "⠙": ("द",), # Letter DA
     "⠮": ("ध",), # Letter DHA
     "⠝": ("न", "ऩ"), # Letter NA and NNNA
     "⠏": ("प",), # Letter PA
     "⠖": ("फ", "फ़"), # Letter PHA and FA
     "⠃": ("ब",), # Letter BA
     "⠘": ("भ",), # Letter BHA
     "⠍": ("म",), # Letter MA
     "⠽": ("य", "य़",), # Letter YA and YYA
     "⠗": ("र", "ऱ"), # Letter RA and RRA
     "⠇": ("ल",), # Letter LA
     "⠸": ("ळ", "ऴ"), # Letter LLA and LLLA
     "⠧": ("व",), # Letter VA
     "⠩": ("श",), # Letter SHA
     "⠯": ("ष",), # Letter SSA
     "⠎": ("स",), # Letter SA
     "⠓": ("ह",), # Letter HA
# Nukta characters that have been assigned separate symbols in Braille
     "⠻": ("ड़",), # Letter DDDHA
     "⠐⠻": ("ढ़",), # Letter RHA
}

## AKHAND LIGATURES
# Akhand ligatures are consonantal ligatures that have a distinct visual form that may not contain the base forms.
# Some of these are represented as unique characters in Bharati Braille.
# They must be converted first; otherwise we'll get an expanded form of these conjuncts in the Braille transcription.
dv_akhand = {
    # क्ष = क + ् + ष
     "⠟": ("क्ष",),
    # ज्ञ = ज + ् + ञ
     "⠱": ("ज्ञ",),
}


## Devanagari characters that have no mapping.
# This isn't used anywhere yet. It exists only for documentation.
# Haven't reviewed these yet.
dv_without_mapping = [
    # Characters which could be shoved somewhere else, just not sure where:
    ("ऄ", "ॻ", "ॼ", "ॾ", "ॿ", "ॽ"),
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
