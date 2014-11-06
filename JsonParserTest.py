__author__ = 'gzs3049'
# coding=utf-8

import unittest
from JsonParser import JsonParser
import json


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.jp = JsonParser()
        self.ocontent = '{"a":"b","c":"d"}'
        self.acontent = '["a","b","c","d"]'
        self.utfstring = u"中文"
        self.complex_json = '{"a":["a","b","c","d"],"c":"d"}'

    def test_getlist(self):
        liststr = r'''{"key":{"integer": 1234567890,
        "real": -9876.543210,
        "e": 0.123456789e-12,
        "E": 1.234567890E+34,
        "":  23456789012E666,
        "zero": 0,
        "one": 1,
        "space": " ",
        "quote": "\"",
        "backslash": "\\",
        "unicode":"\uedda",
        "controls": "\b\f\n\r\t"}}'''
        import json

        data = json.loads(liststr)
        print json.dumps(data)

    def test_getchar(self):
        c = r'\ude1c'
        expected = r'de1c'
        result, index = self.jp.getchar(c, 2)
        print result
        self.assertEqual(expected, result)

    def test_getstring(self):
        s = r'     "\t\\\"t\b\f  \uF234"      '
        expected = r'\t\\\"t\b\f  \uF234'
        result, index = self.jp.getstring(s, 0)
        self.assertEqual(expected, result)

    def test_getnumber(self):
        s1 = r'-0.123'
        e1 = -0.123
        s2 = r'0.123456789E1'
        e2 = 1.23456789
        s3 = r'1231235234234234'
        e3 = 1231235234234234L
        s4 = r'-0'
        e4 = 0
        self.assertEqual(self.jp.getnumber(s1, 0)[0], e1)
        self.assertEqual(self.jp.getnumber(s2, 0)[0], e2)
        self.assertEqual(self.jp.getnumber(s3, 0)[0], e3)
        self.assertEqual(self.jp.getnumber(s4, 0)[0], e4)


if __name__ == '__main__':
    unittest.main()
