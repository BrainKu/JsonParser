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

    # def test_something(self):
    # self.assertEqual(True, True)

    def test_content(self):
        self.assertTrue(JsonParser.check_is_object(self.ocontent))
        self.assertTrue(JsonParser.check_is_array(self.acontent))

    # def test_scanonce(self):
    # invalidstr = "{}"
    # self.assertRaises(SyntaxError, self.jp.scanonce, invalidstr)

    # def test_is_valid_object(self):
    # o1 = '{"key":"value","key2":"value2"}'
    # o2 = '{"key":"[value1, value2]","key2":"value3"}'
    # invalido1 = '{123:"value","key2","333"}'
    #
    # self.assertTrue(JsonParser.check_is_object(o1))
    # self.assertTrue(JsonParser.check_is_object(o2))
    # succeed = True
    # try:
    # self.assertFalse(JsonParser.check_is_object(invalido1))
    # except Exception:
    # succeed = False
    # self.assertFalse(succeed)

    def test_value_is_list(self):
        validstr = "[123,333,\"content\",false,null]"

    def test_value_is_number(self):
        numbers = [12345, -12345, -123456.123, -23e10, -23E10, -23.1e10, "-23.1e-10", "-23.1e+20"]
        for number in numbers:
            self.assertTrue(JsonParser.check_is_number(number))


if __name__ == '__main__':
    unittest.main()
