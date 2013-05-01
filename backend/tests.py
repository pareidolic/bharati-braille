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
# Tests for the Devanagari Unicode to Bharati Braille convertor
#

import sys
import unittest

if sys.version_info.major != 3:
    raise Exception("This program needs Python 3!")

ACHARYA_DEVA_INPUT = \
"""वन्दे मातरं वन्दे मातरम्
सुजलां सुफलां मलयज शीतलाम्
शश्य श्यामलां मातरं वन्दे मातरम्।
सुब्रज्योत्स्ना पुलकित यामिनीम्
पुल्ल कुसुमित द्रुमदल शोभिनीम्
सुहासिनीं सुमधुर भाषिनीम्
सुखदां वरदां मातरं वन्दे मातरम्।"""

ACHARYA_DEVA_OUTPUT = \
"""⠧⠈⠝⠙⠑ ⠍⠜⠞⠗⠰ ⠧⠈⠝⠙⠑ ⠍⠜⠞⠗⠈⠍
⠎⠥⠚⠇⠜⠰ ⠎⠥⠖⠇⠜⠰ ⠍⠇⠽⠚ ⠩⠔⠞⠇⠜⠈⠍
⠩⠈⠩⠽ ⠈⠩⠽⠜⠍⠇⠜⠰ ⠍⠜⠞⠗⠰ ⠧⠈⠝⠙⠑ ⠍⠜⠞⠗⠈⠍⠲
⠎⠥⠈⠃⠗⠈⠚⠽⠕⠈⠞⠈⠎⠝⠜ ⠏⠥⠇⠅⠊⠞ ⠽⠜⠍⠊⠝⠔⠈⠍
⠏⠥⠈⠇⠇ ⠅⠥⠎⠥⠍⠊⠞ ⠈⠙⠗⠥⠍⠙⠇ ⠩⠕⠘⠊⠝⠔⠈⠍
⠎⠥⠓⠜⠎⠊⠝⠔⠰ ⠎⠥⠍⠮⠥⠗ ⠘⠜⠯⠊⠝⠔⠈⠍
⠎⠥⠨⠙⠜⠰ ⠧⠗⠙⠜⠰ ⠍⠜⠞⠗⠰ ⠧⠈⠝⠙⠑ ⠍⠜⠞⠗⠈⠍⠲"""

# Test text from the Bharati Braille Shikshak
SHIKSHAK_INPUT = \
"""(क) २६ जनवरी, ’13 को प्रातःकाल 6:15 बजे से गणतंत्र दिवस शुरू; और रात्रि 11:00 बजे ख़तम।
(ख) उसने पुछा, “आप कौन हैं?!” मैंने कहा “पता नहीं…”"""

SHIKSHAK_OUTPUT = \
"""⠶⠅⠶ ⠼⠃⠋ ⠚⠝⠧⠗⠔⠼⠂ ⠴⠄⠼⠁⠉ ⠅⠕ ⠈⠏⠗⠜⠞⠠⠅⠜⠇ ⠼⠋⠒⠼⠁⠑ ⠃⠚⠑ ⠎⠑ ⠛⠼⠞⠰⠈⠞⠗ ⠙⠊⠧⠎ ⠩⠥⠗⠳⠆ ⠪⠗ ⠗⠜⠈⠞⠗⠊ ⠼⠁⠁⠒⠼⠚⠚ ⠃⠚⠑ ⠨⠞⠍⠲
⠶⠨⠶ ⠥⠎⠝⠑ ⠏⠥⠡⠜⠼⠂ ⠦⠜⠏ ⠅⠪⠝ ⠓⠌⠰⠦⠖⠴ ⠍⠌⠰⠝⠑ ⠅⠓⠜ ⠦⠏⠞⠜ ⠝⠓⠔⠰⠠⠠⠠⠴"""

class TestDevanagari(unittest.TestCase):
    def test_explicit_schwa(self):
        from converters import insert_explicit_schwa
        SCHWA_INPUT = "सईयाँ अनु बाई बम्बई"
        SCHWA_OUTPUT = "स⠁ईयाँ अनु बाई बम्ब⠁ई"
        self.assertEqual(insert_explicit_schwa (SCHWA_INPUT), SCHWA_OUTPUT)

    def test_virama_reversal(self):
        from converters import virama_reversal
        VIRAMA_INPUT = ""
        VIRAMA_OUTPUT = ""
        self.assertEqual(virama_reversal (VIRAMA_INPUT), VIRAMA_OUTPUT)

    def test_translate_math(self):
        from converters import translate_math
        MATH_INPUT = "333 1,2,2 1,000,000 1.0.4 .8 .1.1 7.6 8. 999, ,555"
        MATH_OUTPUT = "⠼⠉⠉⠉ ⠼⠁⠠⠃⠠⠃ ⠼⠁⠠⠚⠚⠚⠠⠚⠚⠚ ⠼⠁⠨⠚⠨⠙ ⠼⠨⠓ ⠼⠨⠁⠨⠁ ⠼⠛⠨⠋ ⠼⠓. ⠼⠊⠊⠊, ,⠼⠑⠑⠑"
        self.assertEqual(translate_math (MATH_INPUT), MATH_OUTPUT)

    def test_acharya_devanagari_conversion(self):
        from converters import convert_devanagari_to_braille
        self.assertEqual(convert_devanagari_to_braille (ACHARYA_DEVA_INPUT)[0], ACHARYA_DEVA_OUTPUT)

    def test_shikshak_conversion(self):
        from converters import convert_devanagari_to_braille
        self.assertEqual(convert_devanagari_to_braille (SHIKSHAK_INPUT)[0], SHIKSHAK_OUTPUT)

if __name__ == "__main__":
    unittest.main(verbosity=2)
