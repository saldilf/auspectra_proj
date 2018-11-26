#!/usr/bin/env python3
"""
Unit and regression test for the auspectra_proj package.
"""

# Import package, test suite, and other packages as needed
# import sys
# import unittest
# from contextlib import contextmanager
# from io import StringIO
#
# from auspectra_proj import main
#

import unittest
import os
import auspectra_proj
# from auspectra696 import main
import xlrd
from auspectra_proj import parse_cmdline
# from au_spectra696.auspectra696 import main
import logging

__author__ = 'salwan'

# Directories #
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

# Input files #
EXCEL_INPUT = os.path.join(DATA_DIR, "LongerTest.xlsx")

# prepare some parameters for use in testing functions
x = 5  # must be in index range of analyzed columns
wb_data = xlrd.open_workbook(EXCEL_INPUT)
sheet1 = wb_data.sheet_by_index(0)
r = sheet1.nrows
c = sheet1.ncols
xLimLflt = sheet1.cell(1, 0).value  # must be less than 400
xLimL = int(xLimLflt)
xLimUflt = sheet1.cell(r - 1, 0).value
xLimU = int(xLimUflt)
lambdas = sheet1.col_values(colx=0, start_rowx=(xLimU - 299) - xLimL, end_rowx=r)  # x-vals (wavelength)
abso = sheet1.col_values(colx=x, start_rowx=(xLimU - 299) - xLimL, end_rowx=r)  # y-vals (absorbance)


class Testauspectra696(unittest.TestCase):

    # test the normalization function
    def test_norm(self):
        result = auspectra_proj.norm(abso, max(abso), x)
        resultF = max(result)
        self.assertEqual(resultF, 1)

    # test the data_analysis function
    def test_data_analysis(self):
        result = auspectra_proj.data_analysis('data/LongerTest.xlsx')
        resultJ = result['Amax']
        self.assertEqual(resultJ, [0.01287, 0.20669, 0.21599, 0.21233, 0.20997,
                                   0.21041, 0.22364, 0.19213, 0.2101, 0.20578,
                                   0.18737, 0.20889, 0.19202])

    # test the normalized data_analysis function
    def test_data_analysisNorm(self):
        result = auspectra_proj.data_analysisNorm('data/LongerTest.xlsx')
        resultJ = result['Amax']
        self.assertEqual(resultJ, [0.01287, 0.20669, 0.21599, 0.21233, 0.20997,
                                   0.21041, 0.22364, 0.19213, 0.2101, 0.20578,
                                   0.18737, 0.20889, 0.19202])

    # test that file entry works


class Test_parse_cmdline(unittest.TestCase):
    def testOneFileInput(self):
        test_input = ['-w', 'data/LongerTest.xlsx']
        foo = parse_cmdline(test_input)
        # vars(test_input)
        # cmdlineVars = vars(parse_cmdline(test_input))
        self.assertTrue(parse_cmdline(test_input)[0]['workbook'] == 'data/LongerTest.xlsx')



if __name__ == '__main__':
    unittest.main()
