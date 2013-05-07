#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set sts=4 sw=4 et :

# Authors:
#  Pooja Saxena <anexasajoop@gmail.com>  

# License:
#  AGPL-3
#  http://www.gnu.org/licenses/agpl-3.0.html



# References and resources used:
# 1. Ahuja, Swaran (2012) Bharati Braille Shikshak. National Association for the Blind, Mumbai.
# 2. Nakanishi, Akira (1992) Writing Systems of the World — Alphabets • Syllabaries • Pictograms. Charles E Tuttle Company, Tokyo.
# 3. Unicode Code Chart for Tamil    Range: 0B80–0BFF [http://www.unicode.org/charts/PDF/U0A80.pdf]
# 4. Unicode Code Chart for Braille Patterns Range: 2800–28FF [http://www.unicode.org/charts/PDF/U2800.pdf]
# 5. “Braille” on Wikipedia [http://en.wikipedia.org/wiki/Braille]



############################################
# Tamil Unicode to Bharati Braille Mapping #
############################################



## VIRAMA
# This is used for the "virama-reversal". See converter.py.
ta_virama = "⠈"


## SCHWA
# This is used for the consonant-vowel idiosyncracy. See converter.py
ta_schwa = "⠁"


## VOWELS AND VOWEL SIGNS
# In Bharati Braille, vowels and their corresponding
# vowel signs are represented by the same Braille pattern.
ta_vowels = {
   "⠁": ("அ",), # Letter A
   "⠜": ("ஆ","ா"), # Letter AA
   "⠊": ("இ","ி"), # Letter I
   "⠔": ("ஈ","ீ"), # Letter II
   "⠥": ("உ","ு"), # Letter U
   "⠳": ("ஊ","ூ"), # Letter UU
   "⠢": ("எ","ெ"), # Letter E
   "⠑": ("ஏ","ே"), # Letter EE
   "⠌": ("ஐ","ை"), # Letter AI
   "⠭": ("ஒ","ொ"), # Letter O
   "⠕": ("ஓ","ோ"), # Letter OO
   "⠪": ("ஔ","ௌ"), # Letter AU
}


## CONSONANTS
ta_consonants = {
    "⠅": ("க",), # Letter KA
    "⠬": ("ங",), # Letter NGA
    "⠉": ("ச",), # Letter CA
    "⠚": ("ஜ",), # Letter JA
    "⠒": ("ஞ",), # Letter NYA
    "⠾": ("ட",), # Letter TTA
    "⠼": ("ண",), # Letter NNA
    "⠞": ("த",), # Letter TA
    "⠝": ("ந",), # Letter NA
    "": ("ன",), # Letter NNA, not assigned in NAB Bharati Braille
    "⠏": ("ப",), # Letter PA
    "⠍": ("ம",), # Letter MA
    "⠽": ("ய",), # Letter YA
    "⠗": ("ர",), # Letter RA
    "⠻": ("ற",), # Letter RRA
    "⠇": ("ல",), # Letter LA
    "⠸": ("ள",), # Letter LLA
    "⠷": ("ழ",), # Letter LLLA
    "⠧": ("வ",), # Letter VA
    "": ("ஶ",), # Letter SHA, not assigned in NAB Bharati Braille
    "⠯": ("ஷ",), # Letter SSA
    "⠎": ("ஸ",), # Letter SA
    "⠓": ("ஹ",), # Letter HA
}


## VARIOUS SIGNS
#Tamil doesn't use anusvara, but it is encoded in Unicode
ta_various_signs = {
    "⠈": ("்",), # Virama, because there is no mapping earlier
    "⠰": ("ௗ",), # Length AU Mark
    "⠠": ("ஃ",), # Visarga
}


## AKHAND LIGATURES
# Akhand ligatures are consonantal ligatures that have a distinct visual form that may not contain the base forms.
# Some of these are represented as unique characters in Bharati Braille.
# They must be converted first; otherwise we'll get an expanded form of these conjuncts in the Braille transcription.
ta_akhand = {
    # க்ஷ = க + ் + ஷ
     "⠟": ("க்ஷ",), 
}


## CHARACTERS THAT ARE NOT ASSIGNED IN BHARATI BRAILLE
# Anusvara, Om, numerics, symbols and currency symbol
ta_without_mapping = [
    ("ஂ", "ௐ", "௰", "௱", "௲", "௳", "௴", "௵", "௶", "௷", "௸", "௺", "௹", )
]