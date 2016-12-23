#! /usr/bin/python
# --*-- coding:utf-8 --*--
u"""
Test code
"""

import unittest
import pycubicspline


class Test(unittest.TestCase):

    def test_param(self):
        x = [-0.5, 0.0, 0.5, 1.0, 1.5]
        y = [3.2, 2.7, 6, 5, 6.5]
        sp = pycubicspline.Spline(x, y)
        self.assertEqual(sp.a[0], 3.2)
        self.assertEqual(sp.a[1], 2.7)
        self.assertEqual(sp.a[2], 6.0)
        self.assertEqual(sp.a[3], 5.0)

        self.assertEqual(sp.b[0], -3.7392857142857139)
        self.assertEqual(sp.b[1], 4.4785714285714278)
        self.assertEqual(sp.b[2], 2.6249999999999991)


if __name__ == '__main__':
    unittest.main()
