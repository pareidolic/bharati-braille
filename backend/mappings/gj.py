#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set sts=4 sw=4 et :

# Authors:
#  Pooja Saxena <anexasajoop@gmail.com>  

# License:
#  AGPL-3
#  http://www.gnu.org/licenses/agpl-3.0.html



###############################################
# Gujarati Unicode to Bharati Braille Mapping #
###############################################



# References and resources used:
# 1. Ahuja, Swaran (2012) Bharati Braille Shikshak. National Association for the Blind, Mumbai.
# 2. Nakanishi, Akira (1992) Writing Systems of the World — Alphabets • Syllabaries • Pictograms. Charles E Tuttle Company, Tokyo.
# 3. Unicode Code Chart for Gujarati Range: 0A80–0AFF [http://www.unicode.org/charts/PDF/U0A80.pdf]
# 4. Unicode Code Chart for Braille Patterns Range: 2800–28FF [http://www.unicode.org/charts/PDF/U2800.pdf]
# 5. “Braille” on Wikipedia [http://en.wikipedia.org/wiki/Braille]



## VIRAMA
# This is used for the "virama-reversal". See converter.py.
gj_virama = "⠈"

## SCHWA
# This is used for the consonant-vowel idiosyncracy. See converter.py
gj_schwa = "⠁"

## VOWELS AND VOWEL SIGNS
# Various signs added here as Unicode escape codes because several scripts
# have the same signs, and they look very similar.
# Done to ensure accuracy.
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
# have the same signs, and they look very similar.
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

## CHARACTERS THAT ARE NOT ASSIGNED IN BHARATI BRAILLE

gj_without_mapping = {
    "ઌ", "ૐ", "ૡ", "ૢ", "ૣ", "૰", "૱"
}