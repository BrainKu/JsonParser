__author__ = 'gzs3049'
# coding=utf-8

import unittest
from JsonParser import JsonParser


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
        result, string = self.jp.getstring(r'"  ",.', 0)
        print type(result), result

    def test_getnumber(self):
        fail = r'0013'
        success = r'-123.123E-10'


if __name__ == '__main__':
    unittest.main()
