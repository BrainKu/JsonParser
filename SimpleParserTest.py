__author__ = 'gzs3049'

import unittest
from SimpleParser import SimpleParser
import json


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.sp = SimpleParser()

    def test_list(self):
        objlist = ['["abc","cde","efg",null,true,false]',
                   '["abc",["efg"]]',
                   '["abc",["abc",null,[false,  null, true]]]']
        for obj in objlist:
            olist, index = self.sp.getlist(1, obj)
            self.assertIsNotNone(olist)
            # print olist

        invalidlist = ['[,,,', '[abcdf']
        for obj in invalidlist:
            self.assertRaises(SyntaxError, self.sp.getlist, 1, obj)

    def test_object(self):
        objlist = ['{"k":"v"}',
                   '{"k":"v","k1":"v"}',
                   '{"k":"v","k1":{"k1":{"k1":"v"}}}',
                   '{"k":[true, false, null]}',
                   '{"k":     null   }']
        for obj in objlist:
            robj, idx = self.sp.getobject(1, obj)
            self.assertIsNotNone(robj)
            # print robj

    def test_number(self):
        numbers = ['12345', '-12345', '-123e10', '-123E10', '-123E-10', '10.1', '10.1e20']
        for number in numbers:
            num, idx = self.sp.getnumber(0, number)
            self.assertIsNotNone(num)
            print "Pair: {} : {}".format(number, num)

    def test_innerconver(self):
        numbers = ['12345', '-12345', '-123e10', '-123E10', '-123E-10', '10.1', '10.1e20']
        for number in numbers:
            num = float(number)
            print "Pair: {} : {}".format(number, num)

    def test_innerjson(self):
        numbers = '[12345, -12345, -123e10, -123E100, -123E-10, 10.1, 10.1e20]'
        print json.loads(numbers)

if __name__ == '__main__':
    unittest.main()
