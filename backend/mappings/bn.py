#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set sts=4 sw=4 et :

# Authors:
#  Pooja Saxena <anexasajoop@gmail.com> 
#  Nirbheek Chauhan <nirbheek.chauhan@gmail.com>

# License:
#  AGPL-3
#  http://www.gnu.org/licenses/agpl-3.0.html



##############################################
# Bengali Unicode to Bharati Braille Mapping #
##############################################



# References and resources used:
# 1. Ahuja, Swaran (2012) Bharati Braille Shikshak. National Association for the Blind, Mumbai.
# 2. Nakanishi, Akira (1992) Writing Systems of the World — Alphabets • Syllabaries • Pictograms. Charles E Tuttle Company, Tokyo.
# 3. Unicode Code Chart for Bengali Range: 0980–09FF [http://www.unicode.org/charts/PDF/U0980.pdf]
# 4. Unicode Code Chart for Braille Patterns Range: 2800–28FF [http://www.unicode.org/charts/PDF/U2800.pdf]
# 5. “Braille” on Wikipedia [http://en.wikipedia.org/wiki/Braille]



## VIRAMA
# This is used for the "virama-reversal". See converter.py.
bn_virama = "⠈"

## SCHWA
# This is used for the "consonant-vowel idiosyncracy". See converter.py
bn_schwa = "⠁"

## VARIOUS SIGNS
# Various signs added here as Unicode escape codes because several scripts
# have the same signs, and they look very similar.
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
# In Bharati Braille, each vowel and its corresponding vowel sign (or matra) is represented by the same Braille character.
# Always put the vowel first, matra second.
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
     "⠕": ("ও", "ো"), # Letter O
     "⠪": ("ঔ", "ৌ"), # Letter AU
} 

## CONSONANTS
# The consonant must always be a single unicode code; not composed from multiple
# unicode codes.
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
# Nukta letters that have been assigned separate symbols in Braille
     "⠻": ("ড়",), # Letter RRA seems to be mapped in the NAB Braille Shikshak as
                  # the Bengali equivalent of ड़ which is the letter DDDHA.
                  # This needs to be double-checked.
     "⠐⠻": ("ঢ়",), # Letter RHA
     "⠢": ("য়",) # Letter YYA
}


## COMPOSITE LETTERS
# Letters that can also be composed from multiple unicode characters; usually by
# combining a nukta with the base letter. These must be converted at the same 
# time as the Akhand ligatures.
# These are different from Akhand ligatures in that these can also be
# represented by a single unicode point. See the list of consonants above.
bn_composite_letters = {
     "⠻": ("\u09A1\u09BC",), #  Letter RRA
     "⠐⠻": ("\u09A2\u09BC",), # Letter RHA
     "⠢": ("\u09AF\u09BC",) # Letter YYA
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


## Are Bengali BA and VA represented by the same letter? Reference needed.
# The Shikshak assigns different cells to BA and VA, but the Unicode chart only has a BA


## CHARACTERS THAT ARE NOT ASSIGNED IN BHARATI BRAILLE

bn_without_mapping = [
    # Bengali nukta, Letter KHANDA TA, length mark, additions for Assamese, currency signs, historical symbols for fractions, other historic signs
    ("়", "ৎ", "ৗ", "ৰ", "ৱ", "৲", "৳", "৴", "৵", "৶", "৷", "৸", "৹", "৺", "৻",),
]
