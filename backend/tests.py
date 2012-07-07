#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set sts=4 sw=4 et :
#
# Author:
#  Nirbheek Chauhan <nirbheek.chauhan@gmail.com>
# License:
#  CC BY-SA
#  http://creativecommons.org/licenses/by-sa/3.0/
#
# Tests for the Devanagari Unicode to Bharati Braille convertor
#

import sys
import unittest

if sys.version_info.major != 3:
    raise Exception("This program needs Python 3!")

TEST_DEVA_INPUT = \
"""वन्दे मातरं वन्दे मातरम्
सुजलां सुफलां मलयज शीतलाम्
शश्य श्यामलां मातरं वन्दे मातरम्।
सुब्रज्योत्स्ना पुलकित यामिनीम्
पुल्ल कुसुमित द्रुमदल शोभिनीम्
सुहासिनीं सुमधुर भाषिनीम्
सुखदां वरदां मातरं वन्दे मातरम्।"""

EXPECTED_DEVA_OUTPUT = \
"""⠧⠈⠝⠙⠑ ⠍⠜⠞⠗⠰ ⠧⠈⠝⠙⠑ ⠍⠜⠞⠗⠈⠍
⠎⠥⠚⠇⠜⠰ ⠎⠥⠖⠇⠜⠰ ⠍⠇⠽⠚ ⠩⠔⠞⠇⠜⠈⠍
⠩⠈⠩⠽ ⠈⠩⠽⠜⠍⠇⠜⠰ ⠍⠜⠞⠗⠰ ⠧⠈⠝⠙⠑ ⠍⠜⠞⠗⠈⠍⠲
⠎⠥⠈⠃⠗⠈⠚⠽⠕⠈⠞⠈⠎⠝⠜ ⠏⠥⠇⠅⠊⠞ ⠽⠜⠍⠊⠝⠔⠈⠍
⠏⠥⠈⠇⠇ ⠅⠥⠎⠥⠍⠊⠞ ⠈⠙⠗⠥⠍⠙⠇ ⠩⠕⠘⠊⠝⠔⠈⠍
⠎⠥⠓⠜⠎⠊⠝⠔⠰ ⠎⠥⠍⠮⠥⠗ ⠘⠜⠯⠊⠝⠔⠈⠍
⠎⠥⠨⠙⠜⠰ ⠧⠗⠙⠜⠰ ⠍⠜⠞⠗⠰ ⠧⠈⠝⠙⠑ ⠍⠜⠞⠗⠈⠍⠲"""

class TestConversions(unittest.TestCase):
    def test_devanagari_conversion(self):
        from converters import convert_devanagari_to_braille
        self.assertEqual(convert_devanagari_to_braille (TEST_DEVA_INPUT),
                          EXPECTED_DEVA_OUTPUT)

if __name__ == "__main__":
    unittest.main(verbosity=2)
