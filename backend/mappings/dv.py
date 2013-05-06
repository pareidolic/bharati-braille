#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set sts=4 sw=4 et :

# Authors:
#  Nirbheek Chauhan <nirbheek.chauhan@gmail.com>
#  Pooja Saxena <anexasajoop@gmail.com>  

# License:
#  AGPL-3
#  http://www.gnu.org/licenses/agpl-3.0.html



#################################################
# Devanagari Unicode to Bharati Braille Mapping #
#################################################


 
# References and resources used:
# 1. Ahuja, Swaran (2012) Bharati Braille Shikshak. National Association for the Blind, Mumbai.
# 2. Nakanishi, Akira (1992) Writing Systems of the World — Alphabets • Syllabaries • Pictograms. Charles E Tuttle Company, Tokyo.
# 3. Unicode Code Chart for Devanagari Range: 0900–097F [http://www.unicode.org/charts/PDF/U0900.pdf]
# 4. Unicode Code Chart for Braille Patterns Range: 2800–28FF [http://www.unicode.org/charts/PDF/U2800.pdf]
# 5. “Braille” on Wikipedia [http://en.wikipedia.org/wiki/Braille]



## VIRAMA
# This is used for the "virama-reversal". See converter.py.
dv_virama = "⠈"


## SCHWA
# This is used for the consonant-vowel idiosyncracy. See converter.py
dv_schwa = "⠁"


## VARIOUS SIGNS
# Various signs added here as Unicode escape codes because several scripts
# have the same signs, and they look very similar.
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
# Always put the vowel first, matra second.
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
# Those nukta characters with no special cell assigned are being collapsed with their base letter
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
     "⠟": ("क्ष",), # Conjunct KSSA
    # ज्ञ = ज + ् + ञ
     "⠱": ("ज्ञ",), # Conjunct JNYA
}


## CHARACTERS THAT ARE NOT ASSIGNED IN BHARATI BRAILLE

dv_without_mapping = [

    # Devanagari 0900-097F:
    ("ऄ", "ॻ", "ॼ", "ॾ", "ॿ", "ॽ","ऀ", "ऺ", "ऻ", "़", "ॎ", "ॏ", "ॐ", "॑", "॒", "॓", "॔", "ॕ", "ॖ", "ॗ", "॰",
     "ॱ", "ॳ", "ॴ", "ॵ", "ॶ", "ॷ", "ॹ", "ॺ",),

    # Devanagari Extended:
    ("꣠", "꣡", "꣢", "꣣", "꣤", "꣥", "꣦", "꣧", "꣨", "꣩", "꣪", "꣫", "꣬", "꣭", "꣮",
     "꣯", "꣰", "꣱", ",ꣲ", "ꣳ", "ꣴ", "ꣵ", "ꣶ", "ꣷ", "꣸", "꣹", "꣺", "ꣻ"),
    
    # Vedic Extensions:
    ("᳐", "᳑", "᳒", "᳓", "᳔", "᳕", "᳖", "᳗", "᳘", "᳙", "᳚", "᳛", "᳜", "᳝", "᳞",
     "᳟", "᳠", "᳡", "᳢", "᳣", "᳤", "᳥", "᳦", "᳧", "᳨", "ᳩ", "ᳪ", "ᳫ", "ᳬ", "᳭",
     "ᳮ", "ᳯ", "ᳰ", "ᳱ", "ᳲ", "ᳳ", "᳴", "ᳵ", "ᳶ"),
]
