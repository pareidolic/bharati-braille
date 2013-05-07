#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set sts=4 sw=4 et :

# Author:
#  Pooja Saxena <anexasajoop@gmail.com>  

# License:
#  AGPL-3
#  http://www.gnu.org/licenses/agpl-3.0.html



#############################################
# Telugu Unicode to Bharati Braille Mapping #
#############################################



# References and resources used:
# 1. Ahuja, Swaran (2012) Bharati Braille Shikshak. National Association for the Blind, Mumbai.
# 2. Nakanishi, Akira (1992) Writing Systems of the World — Alphabets • Syllabaries • Pictograms. Charles E Tuttle Company, Tokyo.
# 3. Unicode Code Chart for Telugu Range: 0C00–0C7F [http://www.unicode.org/charts/PDF/U0C00.pdf]
# 4. Unicode Code Chart for Braille Patterns Range: 2800–28FF [http://www.unicode.org/charts/PDF/U2800.pdf]
# 5. “Braille” on Wikipedia [http://en.wikipedia.org/wiki/Braille]



## VIRAMA
# This is used for the "virama-reversal". See converter.py.
te_virama = "⠈"


## SCHWA
# This is used for the "consonant-vowel idiosyncracy". See converter.py
te_schwa = "⠁"


## VARIOUS SIGNS
# Various signs added here as Unicode escape codes because several scripts
# have the same signs, and they look very similar.
# Done to ensure accuracy.
te_various_signs = {
    "⠈": ("\u0C4D",), #Virama
    "": ("\u0C3D",), # Avagraha (same mapping as comma?), *Not assigned for Telugu*
    "⠄": ("\u0C01",), # Chandra-bindu
    "⠰": ("\u0C02",), # Anusvara    
    "⠠": ("\u0C03",), # Visarga
    #"": ("",), # There is no Nukta in Telugu
}

## VOWELS AND VOWEL SIGNS
# In Bharati Braille, each vowel and its corresponding vowel sign (or matra) is represented by the same Braille character.
# Always put the vowel first, matra second.
te_vowels = {
     # The schwa vowel is inherent in every consonant, and does not have a separate vowel sign.
     "⠁": ("అ",), # Letter A
     "⠜": ("ఆ", "ా" ), # Letter AA
     "⠊": ("ఇ", "ి"), # Letter I
     "⠔": ("ఈ", "ీ"), # Letter II
     "⠥": ("ఉ", "ు"), # Letter U
     "⠳": ("ఊ", "ూ"), # Letter UU
     "⠐⠗": ("ఋ", "ృ"), # Letter Vocalic R, 
     "⠠⠗": ("ౠ","ౄ"), # Letter Vocalic RR
     "⠐⠇": ("ఌ","\u0C62"), # Letter Vocalic L, *Couldn't copy vowel sign, pasted unicode escape code instead*
     "⠠⠇": ("ౡ","\u0C63"), # Letter Vocalic LL *Couldn't copy vowel sign, pasted unicode escape code instead*
     "⠢": ("ఎ","ె"), # Letter E
     "⠑": ("ఏ","ే"), # Letter EE
     "⠌": ("ఐ","ై"), # Letter AI
     "⠭": ("ఒ","ొ"), # Letter O
     "⠕": ("ఓ","ో"), # Letter OO
     "⠪": ("ఔ","ౌ"), # Letter AU
} 

## CONSONANTS
te_consonants = {
     "⠅": ("క",), # Letter KA
     "⠨": ("ఖ",), # Letter KHA
     "⠛": ("గ",), # Letter GA
     "⠣": ("ఘ",), # Letter GHA
     "⠬": ("ఙ",), # Letter NGA
     "⠉": ("చ",), # Letter CA
     "⠡": ("ఛ",), # Letter CHA
     "⠚": ("జ",), # Letter JA
     "⠴": ("ఝ",), # Letter JHA
     "⠒": ("ఞ",), # Letter NYA
     "⠾": ("ట",), # Letter TTA
     "⠺": ("ఠ",), # Letter TTHA
     "⠫": ("డ",), # Letter DDA
     "⠿": ("ఢ",), # Letter DDHA
     "⠼": ("ణ",), # Letter NNA
     "⠞": ("త",), # Letter TA
     "⠹": ("థ",), # Letter THA
     "⠙": ("ద",), # Letter DA
     "⠮": ("ధ",), # Letter DHA
     "⠝": ("న",), # Letter NA
     "⠏": ("ప",), # Letter PA
     "⠖": ("ఫ",), # Letter PHA
     "⠃": ("బ",), # Letter BA
     "⠘": ("భ",), # Letter BHA
     "⠍": ("మ",), # Letter MA
     "⠽": ("య",), # Letter YA
     "⠗": ("ర",), # Letter RA
     #"": ("",),  # Letter RRA, not assigned in Bharati Braille
     "⠇": ("ల",), # Letter LA
     "⠸": ("ళ",), # Letter LLA
     "⠧": ("వ",), # Letter VA
     "⠩": ("శ",), # Letter SHA
     "⠯": ("ష",), # Letter SSA
     "⠎": ("స",), # Letter SA
     "⠓": ("హ",), # Letter HA
}

## AKHAND LIGATURES
# Akhand ligatures are consonantal ligatures that have a distinct visual form that may not contain the base forms.
# Some of these are represented as unique characters in Bharati Braille.
# They must be converted first; otherwise we'll get an expanded form of these conjuncts in the Braille transcription.
te_akhand = {
    # క్ష = క + ్ + ష
     "⠟": ("క్ష",), # Conjunct KSSA
}

## CHARACTERS MISSING IN UNICODE CHART
# Couldn't find the Telugu equivalent of ड़ in the Unicode, it is assigned a cell in Bharati Braille
# See Bharati Braille Shikshak, p79.
# Could it possibly be the LETTER RRA?

## CHARACTERS THAT ARE NOT ASSIGNED IN BHARATI BRAILLE

te_without_mapping = [

    # Letter RRA, length marks, historic phonetic variants, fractions and weights
    ("\u0C31", "\u0C55", "\u0C56", "\u0C58", "\u0C59", "\u0C78", "\u0C79", "\u0C7A", "\u0C7B", "\u0C7C", "\u0C7D", "\u0C7E","\u0C7F"),
]
