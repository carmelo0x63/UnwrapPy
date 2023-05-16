#!/usr/bin/env python3
import unittest
import unwrapurl

global ISVERBOSE
ISVERBOSE = 0

class testURL(unittest.TestCase):
    def test_bit_ly(self):
        self.assertEqual(unwrapurl.findLocation('https://bit.ly/3ABvcy5')[0], 'https://isc.sans.edu/')

if __name__ == '__main__':
    unittest.main()

