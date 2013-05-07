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
# Tests for the Devanagari Unicode to Bharati Braille convertor
#

import sys
import unittest

if sys.version_info.major != 3:
    raise Exception("This program needs Python 3!")

DV_ACHARYA_INPUT = \
"""वन्दे मातरं वन्दे मातरम्
सुजलां सुफलां मलयज शीतलाम्
शश्य श्यामलां मातरं वन्दे मातरम्।
सुब्रज्योत्स्ना पुलकित यामिनीम्
पुल्ल कुसुमित द्रुमदल शोभिनीम्
सुहासिनीं सुमधुर भाषिनीम्
सुखदां वरदां मातरं वन्दे मातरम्।"""

DV_ACHARYA_OUTPUT = \
"""⠧⠈⠝⠙⠑ ⠍⠜⠞⠗⠰ ⠧⠈⠝⠙⠑ ⠍⠜⠞⠗⠈⠍
⠎⠥⠚⠇⠜⠰ ⠎⠥⠖⠇⠜⠰ ⠍⠇⠽⠚ ⠩⠔⠞⠇⠜⠈⠍
⠩⠈⠩⠽ ⠈⠩⠽⠜⠍⠇⠜⠰ ⠍⠜⠞⠗⠰ ⠧⠈⠝⠙⠑ ⠍⠜⠞⠗⠈⠍⠲
⠎⠥⠈⠃⠗⠈⠚⠽⠕⠈⠞⠈⠎⠝⠜ ⠏⠥⠇⠅⠊⠞ ⠽⠜⠍⠊⠝⠔⠈⠍
⠏⠥⠈⠇⠇ ⠅⠥⠎⠥⠍⠊⠞ ⠈⠙⠗⠥⠍⠙⠇ ⠩⠕⠘⠊⠝⠔⠈⠍
⠎⠥⠓⠜⠎⠊⠝⠔⠰ ⠎⠥⠍⠮⠥⠗ ⠘⠜⠯⠊⠝⠔⠈⠍
⠎⠥⠨⠙⠜⠰ ⠧⠗⠙⠜⠰ ⠍⠜⠞⠗⠰ ⠧⠈⠝⠙⠑ ⠍⠜⠞⠗⠈⠍⠲"""

# Test text from the Bharati Braille Shikshak
DV_SHIKSHAK_INPUT = \
"""(क) २६ जनवरी, ’13 को प्रातःकाल 6:15 बजे से राष्ट्र गणतंत्र दिवस शुरू; और रात्रि 11:00 बजे ख़तम।
(ख) उसने पुछा, “आप कौन हैं?!” मैंने कहा “पता नहीं…”
शिक्षक"""

DV_SHIKSHAK_OUTPUT = \
"""⠶⠅⠶ ⠼⠃⠋ ⠚⠝⠧⠗⠔⠂ ⠴⠄⠼⠁⠉ ⠅⠕ ⠈⠏⠗⠜⠞⠠⠅⠜⠇ ⠼⠋⠒⠼⠁⠑ ⠃⠚⠑ ⠎⠑ ⠗⠜⠈⠯⠈⠾⠗ ⠛⠼⠞⠰⠈⠞⠗ ⠙⠊⠧⠎ ⠩⠥⠗⠳⠆ ⠪⠗ ⠗⠜⠈⠞⠗⠊ ⠼⠁⠁⠒⠼⠚⠚ ⠃⠚⠑ ⠨⠞⠍⠲
⠶⠨⠶ ⠥⠎⠝⠑ ⠏⠥⠡⠜⠂ ⠦⠜⠏ ⠅⠪⠝ ⠓⠌⠰⠦⠖⠴ ⠍⠌⠰⠝⠑ ⠅⠓⠜ ⠦⠏⠞⠜ ⠝⠓⠔⠰⠠⠠⠠⠴
⠩⠊⠟⠅"""


class TestCommonGlyphs(unittest.TestCase):
    def test_translate_math(self):
        from converters import translate_math
        MATH_INPUT = "333 1,2,2 1,000,000 1.0.4 .8 .1.1 7.6 8. 999, ,555"
        MATH_OUTPUT = "⠼⠉⠉⠉ ⠼⠁⠠⠃⠠⠃ ⠼⠁⠠⠚⠚⠚⠠⠚⠚⠚ ⠼⠁⠨⠚⠨⠙ ⠼⠨⠓ ⠼⠨⠁⠨⠁ ⠼⠛⠨⠋ ⠼⠓. ⠼⠊⠊⠊, ,⠼⠑⠑⠑"
        self.assertEqual(translate_math (MATH_INPUT),
                         MATH_OUTPUT)

    def test_common_glyph_conversion(self):
        from converters import convert_common_glyphs_to_braille
        COMMON_INPUT = "‐ - – — ... … , ; : । ॥ ! ? *"
        COMMON_OUTPUT = "⠤ ⠤ ⠤⠤ ⠤⠤⠤⠤ ⠠⠠⠠ ⠠⠠⠠ ⠂ ⠆ ⠒ ⠲ ⠲⠲ ⠖ ⠦ ⠔⠔"
        self.assertEqual(convert_common_glyphs_to_braille (COMMON_INPUT),
                         COMMON_OUTPUT)

class TestDevanagari(unittest.TestCase):
    def test_explicit_schwa(self):
        from converters import dv_schwa, all_dv_consonants, dv_vowel_chars
        from converters import insert_explicit_schwa
        SCHWA_INPUT = "सईयाँ अनु बाई बम्बई"
        SCHWA_OUTPUT = "स⠁ईयाँ अनु बाई बम्ब⠁ई"
        self.assertEqual(insert_explicit_schwa(SCHWA_INPUT, dv_schwa,
                                               all_dv_consonants,
                                               dv_vowel_chars),
                         SCHWA_OUTPUT)

    def test_virama_reversal(self):
        from converters import dv_virama, virama_reversal
        VIRAMA_INPUT = "⠏⠈\n⠏⠈⠗\n⠏⠈⠗⠈⠞"
        VIRAMA_OUTPUT = "⠈⠏\n⠈⠏⠗\n⠈⠏⠈⠗⠞"
        self.assertEqual(virama_reversal(VIRAMA_INPUT, dv_virama),
                         VIRAMA_OUTPUT)

    def test_acharya_conversion(self):
        from converters import convert_devanagari_to_braille
        self.assertEqual(convert_devanagari_to_braille(DV_ACHARYA_INPUT)[0],
                         DV_ACHARYA_OUTPUT)

    def test_comprehensive_conversion(self):
        from converters import convert_devanagari_to_braille
        self.assertEqual(convert_devanagari_to_braille(DV_SHIKSHAK_INPUT)[0],
                         DV_SHIKSHAK_OUTPUT)

class TestGujarati(unittest.TestCase):
    # TODO: Use Gujarati here and implement everything else
    def test_virama_reversal(self):
        from converters import gu_virama, virama_reversal
        VIRAMA_INPUT = "⠏⠈\n⠏⠈⠗\n⠏⠈⠗⠈⠞"
        VIRAMA_OUTPUT = "⠈⠏\n⠈⠏⠗\n⠈⠏⠈⠗⠞"
        self.assertEqual(virama_reversal(VIRAMA_INPUT, gu_virama),
                         VIRAMA_OUTPUT)

    def test_comprehensive_conversion(self):
        from converters import convert_gujarati_to_braille
        self.assertEqual(convert_gujarati_to_braille("ADD TEST STRING HERE")[0],
                         "ADD TEST STRING HERE")

class TestBengali(unittest.TestCase):
    # TODO: Use Bengali here and implement everything else
    def test_virama_reversal(self):
        from converters import bn_virama, virama_reversal
        VIRAMA_INPUT = "⠏⠈\n⠏⠈⠗\n⠏⠈⠗⠈⠞"
        VIRAMA_OUTPUT = "⠈⠏\n⠈⠏⠗\n⠈⠏⠈⠗⠞"
        self.assertEqual(virama_reversal(VIRAMA_INPUT, bn_virama),
                         VIRAMA_OUTPUT)

    def test_comprehensive_conversion(self):
        from converters import convert_bengali_to_braille
        self.assertEqual(convert_bengali_to_braille("ADD TEST STRING HERE")[0],
                         "ADD TEST STRING HERE")

class TestTelugu(unittest.TestCase):
    def test_virama_reversal(self):
        from converters import te_virama, virama_reversal
        VIRAMA_INPUT = "⠏⠈\n⠏⠈⠗\n⠏⠈⠗⠈⠞"
        VIRAMA_OUTPUT = "⠈⠏\n⠈⠏⠗\n⠈⠏⠈⠗⠞"
        self.assertEqual(virama_reversal (VIRAMA_INPUT, te_virama),
                         VIRAMA_OUTPUT)

    def test_comprehensive_conversion(self):
        from converters import convert_telugu_to_braille
        self.assertEqual(convert_telugu_to_braille ("ADD TEST STRING HERE")[0],
                         "ADD TEST STRING HERE")

class TestAutodetectConverter(unittest.TestCase):
    def test_none_detected(self):
        from converters import convert_any_indic_to_braille, BB_ERR_UNKNOWN_SCRIPT
        (text, warnings) = convert_any_indic_to_braille("Non-indic text")
        self.assertEqual(text, "")
        self.assertEqual(warnings, BB_ERR_UNKNOWN_SCRIPT)

    def test_multiple_detected(self):
        from converters import convert_any_indic_to_braille, BB_ERR_MANY_SCRIPTS
        (text, warnings) = convert_any_indic_to_braille("है ল")
        self.assertEqual(text, "")
        self.assertEqual(warnings, BB_ERR_MANY_SCRIPTS)

    def test_bengali_detected(self):
        from converters import convert_any_indic_to_braille
        input_text = "বাংলা"
        (text, warnings) = convert_any_indic_to_braille(input_text)
        self.assertEqual(warnings, "")
        self.assertNotEqual(text, input_text)

    def test_devanagari_detected(self):
        from converters import convert_any_indic_to_braille
        input_text = "देवनागरी"
        (text, warnings) = convert_any_indic_to_braille(input_text)
        self.assertEqual(warnings, "")
        self.assertNotEqual(text, input_text)

    def test_gujarati_detected(self):
        from converters import convert_any_indic_to_braille
        input_text = "ગુજરાતી"
        (text, warnings) = convert_any_indic_to_braille(input_text)
        self.assertEqual(warnings, "")
        self.assertNotEqual(text, input_text)

    def test_telugu_detected(self):
        from converters import convert_any_indic_to_braille
        input_text = "తెలుగు"
        (text, warnings) = convert_any_indic_to_braille(input_text)
        self.assertEqual(warnings, "")
        self.assertNotEqual(text, input_text)

if __name__ == "__main__":
    unittest.main(verbosity=2)
